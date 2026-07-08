"""
Fluxa CLI - Convert tutorials to Photoshop API JSON
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint
from dotenv import load_dotenv

from .extractors.factory import ExtractorFactory
from .generators.photoshop_action_generator import PhotoshopActionGenerator
from .generators.agent_photoshop_action_generator import AgentPhotoshopActionGenerator
from .utils.formatter import format_output, add_metadata
from .utils.validator import validate_json


# Load environment variables
load_dotenv()

console = Console()


def load_config() -> dict:
    """Load configuration from config file"""
    config_path = Path(__file__).parent.parent.parent / "config" / "default.json"
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception:
        return {
            "openai": {"model": "gpt-5.1", "temperature": 0.1, "max_tokens": 4000, "timeout": 60},
            "output": {"indent": 2, "add_metadata": True, "validate": True},
            "extraction": {"youtube": {"max_transcript_length": 50000}, "web": {"max_content_length": 100000, "timeout": 30}}
        }


@click.command()
@click.argument('url', type=str, required=False)
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path (default: output.json)'
)
@click.option(
    '--model', '-m',
    type=str,
    help='OpenAI model to use (default: gpt-5.1)'
)
@click.option(
    '--api-key',
    type=str,
    envvar='OPENAI_API_KEY',
    help='OpenAI API key (or set OPENAI_API_KEY env variable)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Show detailed processing information'
)
@click.option(
    '--no-metadata',
    is_flag=True,
    help='Do not add metadata to output'
)
@click.option(
    '--no-validate',
    is_flag=True,
    help='Skip validation'
)
@click.option(
    '--estimate-cost',
    is_flag=True,
    help='Show cost estimate and exit without generating'
)
@click.option(
    '--use-agent',
    is_flag=True,
    help='Use agent-based generator with dynamic documentation reading'
)
@click.option(
    '--transcript', '-t',
    type=click.Path(exists=True),
    help='Path to transcript text file (use instead of URL)'
)
def main(
    url: Optional[str],
    output: Optional[str],
    model: Optional[str],
    api_key: Optional[str],
    verbose: bool,
    no_metadata: bool,
    no_validate: bool,
    estimate_cost: bool,
    use_agent: bool,
    transcript: Optional[str]
) -> None:
    """
    Fluxa - Convert Photoshop tutorials to API JSON
    
    Accepts YouTube video URLs, web article URLs, or transcript files
    and generates executable Photoshop API action JSON files.
    
    Examples:
        fluxa https://www.youtube.com/watch?v=... -o actions.json
        fluxa --transcript tutorial.txt -o actions.json --use-agent
    """
    config = load_config()
    
    # Display welcome banner
    console.print(Panel.fit(
        "[bold cyan]Fluxa AI Tool[/bold cyan]\n"
        "Tutorial → Photoshop API JSON",
        border_style="cyan"
    ))
    
    # Validate that either URL or transcript is provided
    if not url and not transcript:
        console.print("[red]Error:[/red] Either URL or --transcript must be provided.", style="bold")
        console.print("\nExamples:")
        console.print("  fluxa https://www.youtube.com/watch?v=... -o actions.json")
        console.print("  fluxa --transcript tutorial.txt -o actions.json --use-agent")
        sys.exit(1)
    
    # Validate API key
    if not api_key:
        console.print("[red]Error:[/red] OpenAI API key not found.", style="bold")
        console.print("Set the OPENAI_API_KEY environment variable or use --api-key option.")
        console.print("\nExample: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    # Set defaults from config
    if not model:
        model = config['openai']['model']
    
    if not output:
        output = 'output.json'
    
    try:
        # Step 1: Extract content (from URL or transcript file)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Extracting tutorial content...", total=None)
            
            try:
                if transcript:
                    # Read transcript from file
                    with open(transcript, 'r', encoding='utf-8') as f:
                        content = f.read()
                    extracted = {
                        'content': content,
                        'source': transcript,
                        'type': 'transcript_file'
                    }
                    console.print(f"[green]✓[/green] Transcript loaded from: {transcript}")
                else:
                    # Extract from URL
                    extracted = ExtractorFactory.extract(url, config['extraction'])
                    console.print("[green]✓[/green] Content extracted successfully")
                
                progress.update(task, completed=True)
                
                if verbose:
                    console.print(f"\n[dim]Source:[/dim] {extracted['source']}")
                    console.print(f"[dim]Type:[/dim] {extracted['type']}")
                    if 'title' in extracted:
                        console.print(f"[dim]Title:[/dim] {extracted['title']}")
                    console.print(f"[dim]Content length:[/dim] {len(extracted['content'])} characters\n")
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]✗[/red] Extraction failed: {str(e)}")
                sys.exit(1)
        
        # Step 2: Initialize generator (agent-based or standard)
        if use_agent:
            console.print("[cyan]Using agent-based generator with dynamic documentation[/cyan]")
            generator = AgentPhotoshopActionGenerator(
                api_key=api_key,
                model=model,
                timeout=config['openai']['timeout']
            )
        else:
            generator = PhotoshopActionGenerator(
                api_key=api_key,
                model=model,
                temperature=config['openai']['temperature'],
                max_tokens=config['openai']['max_tokens'],
                timeout=config['openai']['timeout']
            )
        
        cost_estimate = generator.estimate_cost(len(extracted['content']))
        
        if verbose or estimate_cost:
            console.print("\n[bold]Cost Estimate:[/bold]")
            console.print(f"  Input tokens: ~{cost_estimate['estimated_input_tokens']:,}")
            console.print(f"  Output tokens: ~{cost_estimate['estimated_output_tokens']:,}")
            console.print(f"  Estimated cost: ${cost_estimate['estimated_total_cost']:.4f} USD\n")
        
        if estimate_cost:
            console.print("[dim]Use without --estimate-cost to proceed with generation[/dim]")
            sys.exit(0)
        
        # Step 3: Generate actions
        generation_msg = "[cyan]Generating Photoshop actions with agent..." if use_agent else "[cyan]Generating Photoshop actions with AI..."
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(generation_msg, total=None)
            
            try:
                result = generator.generate(
                    content=extracted['content'],
                    source=extracted['source'],
                    source_type=extracted['type']
                )
                progress.update(task, completed=True)
                console.print("[green]✓[/green] Actions generated successfully")
                
                if verbose:
                    console.print(f"[dim]Model:[/dim] {result['model']}")
                    console.print(f"[dim]Attempts:[/dim] {result['attempt']}")
                    console.print(f"[dim]Actions count:[/dim] {len(result['actions'])}\n")
                
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]✗[/red] Generation failed: {str(e)}")
                sys.exit(1)
        
        # Step 4: Validate
        actions = result['actions']
        validation_errors = result.get('validation_errors', [])
        
        if not no_validate and config['output']['validate']:
            is_valid, errors = validate_json(actions)
            validation_errors.extend(errors)
            
            if validation_errors:
                console.print("\n[yellow]⚠ Validation warnings:[/yellow]")
                for error in validation_errors[:5]:  # Show first 5 errors
                    console.print(f"  • {error}")
                if len(validation_errors) > 5:
                    console.print(f"  [dim]... and {len(validation_errors) - 5} more[/dim]")
                console.print()
            else:
                console.print("[green]✓[/green] Validation passed")
        
        # Step 5: Format output
        if not no_metadata and config['output']['add_metadata']:
            output_data = add_metadata(
                actions,
                source=extracted['source'],
                source_type=extracted['type']
            )
        else:
            output_data = actions
        
        formatted_output = format_output(output_data, indent=config['output']['indent'])
        
        # Step 6: Save to file
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        
        console.print(f"\n[green]✓[/green] Saved to: [bold]{output_path.absolute()}[/bold]")
        
        # Preview output
        if verbose:
            console.print("\n[bold]Preview:[/bold]")
            preview = formatted_output[:500]
            if len(formatted_output) > 500:
                preview += "\n  ..."
            syntax = Syntax(preview, "json", theme="monokai", line_numbers=False)
            console.print(syntax)
        
        console.print("\n[green bold]✓ Complete![/green bold]")
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red bold]Error:[/red bold] {str(e)}")
        if verbose:
            import traceback
            console.print("\n[dim]" + traceback.format_exc() + "[/dim]")
        sys.exit(1)


if __name__ == '__main__':
    main()


