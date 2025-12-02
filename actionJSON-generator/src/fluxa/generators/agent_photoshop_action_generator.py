"""
Agent-based Photoshop Action JSON generator using DeepAgents.

This generator dynamically reads documentation from ps_action_docs/atomic_actions/
instead of using hardcoded prompts, providing more accurate and flexible operation mapping.
"""

import os
import json
import re
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.chat_models import init_chat_model

# Configure logging with immediate flush
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Force immediate flush on all log messages
for handler in logging.root.handlers:
    handler.flush()
    if hasattr(handler, 'stream'):
        handler.stream.flush()


# System prompt for the agent
AGENT_SYSTEM_PROMPT = """You are an expert Photoshop action generator. Your task is to convert tutorial transcripts into Photoshop API ActionJSON format.

## CRITICAL: YOU MUST READ DOCUMENTATION BEFORE GENERATING OUTPUT

**DO NOT generate any JSON output until you have read the relevant documentation files.**

You have access to a documentation folder. You MUST use the filesystem tools to read this documentation before generating any output.

## IMPORTANT: Use relative paths (no leading slash)
- Use `ls .` to list current directory
- Use `read_file atomic_actions/index.md` to see ALL available operations
- Use `read_file atomic_actions/filters/gaussian_blur.md` NOT `read_file /atomic_actions/...`

## MANDATORY WORKFLOW (Follow these steps IN ORDER)

### Step 1: READ THE INDEX FIRST
**ALWAYS start by reading the index file:**
```
read_file atomic_actions/index.md
```
This index contains a complete list of ALL available operations with their exact file paths and descriptions.

### Step 2: Identify operations from the transcript
Analyze the tutorial transcript and match operations to files listed in the index:
- "blur background" → `filters/gaussian_blur.md`
- "select subject" → `selection/select_subject.md`
- "duplicate layer" → `layer_management/duplicate_layer.md`
- "reduce fill" or "fill to 0%" → `layer_management/fill_opacity.md`
- "drag layer under/over" or "reorder" → `layer_management/layer_reorder.md`
- "stroke" or "layer style stroke" → `layer_management/stroke_layer_style.md`
- "clipping mask" → `layer_management/create_clipping_mask.md`
- "link layers" → `layer_management/link_layers.md`
- "convert to smart object" → `layer_management/convert_to_smart_object.md`
- "add text" → `text_layer.md`
- "transform" or "scale" → `layer_management/transform.md`
- "mask" → `layer_management/create_mask.md`

### Step 3: Read the relevant documentation files
For EACH operation you identified, use `read_file` to read the corresponding .md file.
Use the EXACT file paths from the index. For example:
- `read_file atomic_actions/filters/gaussian_blur.md`
- `read_file atomic_actions/layer_management/fill_opacity.md`
- `read_file atomic_actions/layer_management/stroke_layer_style.md`

Each .md file contains the exact JSON structure you need to use.

### Step 4: Generate the ActionJSON
ONLY AFTER reading the documentation, generate the JSON array using the exact formats from the docs.

## Important Rules

1. **NO open/save operations** - Document is already loaded via API
2. **Use ordinal references** for layer selection when possible
3. **Preserve parameter values** from tutorial when specified
4. **Skip non-Photoshop steps** (download, watch video, subscribe, etc.)
5. **Output ONLY valid JSON array** - no explanations, no markdown in the final output

## Output Format

Your FINAL output must be ONLY a JSON array like this:
```json
[
  {"_obj": "brightnessEvent", "brightness": 20, "center": 10, "useLegacy": false},
  {"_obj": "gaussianBlur", "radius": {"_unit": "pixelsUnit", "_value": 5.0}}
]
```

## Multiple Images

If tutorial mentions adding/placing another image:
- Use `placeEvent` with `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_0` for second image
- Use `ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_1` for third image, etc.

## REMEMBER: You MUST read documentation files before generating output. Do not skip this step!
"""


class AgentPhotoshopActionGenerator:
    """
    Generate Photoshop API JSON from tutorial content using DeepAgents.
    
    This class uses DeepAgents with FilesystemBackend to dynamically read
    documentation files and map tutorial steps to ActionJSON operations.
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5.1",
        docs_path: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize the agent-based generator.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-5.1)
            docs_path: Path to ps_action_docs folder (auto-detected if None)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model_name = model
        self.timeout = timeout
        
        # Auto-detect docs path if not provided
        if docs_path is None:
            # Try to find ps_action_docs relative to this file
            current_file = Path(__file__).resolve()
            # Go up from generators/ -> fluxa/ -> src/ -> actionJSON-generator/ -> fluxa/
            project_root = current_file.parent.parent.parent.parent.parent
            self.docs_path = project_root / "ps_action_docs"
            
            if not self.docs_path.exists():
                # Fallback: try current working directory
                self.docs_path = Path.cwd() / "ps_action_docs"
                if not self.docs_path.exists():
                    raise ValueError(
                        f"Could not find ps_action_docs folder. "
                        f"Tried: {project_root / 'ps_action_docs'} and {Path.cwd() / 'ps_action_docs'}"
                    )
        else:
            self.docs_path = Path(docs_path)
        
        self.project_root = self.docs_path.parent
        logger.info(f"Using docs path: {self.docs_path}")
        logger.info(f"Project root: {self.project_root}")
        
        # Set OpenAI API key in environment for LangChain
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize the model
        self.model = init_chat_model(f"openai:{model}")
        
        # Create the agent with FilesystemBackend
        # IMPORTANT: Restrict backend to ps_action_docs folder only
        # This forces the agent to focus on the documentation
        # virtual_mode=True sandboxes all paths under root_dir
        self.backend = FilesystemBackend(root_dir=str(self.docs_path), virtual_mode=True)
        
        logger.info(f"FilesystemBackend created with root_dir: {self.docs_path}")
        logger.info(f"FilesystemBackend cwd: {self.backend.cwd}")
        
        # Test the backend directly
        try:
            test_ls = self.backend.ls_info('.')
            logger.info(f"Backend ls_info('.') test: {[f['path'] for f in test_ls[:3]]}...")
        except Exception as e:
            logger.error(f"Backend ls_info test failed: {e}")
        
        self.agent = create_deep_agent(
            model=self.model,
            backend=self.backend,
            system_prompt=AGENT_SYSTEM_PROMPT,
        )
        
        logger.info(f"Agent FilesystemBackend root: {self.docs_path}")
        logger.info("AgentPhotoshopActionGenerator initialized successfully")
    
    def generate(
        self,
        content: str,
        source: str,
        source_type: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Generate Photoshop actions from tutorial content using the agent.
        
        Args:
            content: Tutorial text content (transcript)
            source: Source URL
            source_type: Type of source (youtube or web)
            max_retries: Maximum retry attempts for failed generations
            
        Returns:
            Dictionary with generated actions and metadata
            
        Raises:
            ValueError: If generation fails after retries
        """
        logger.info(f"Starting agent generation for source: {source}")
        logger.info(f"Content length: {len(content)} characters")
        logger.info(f"=== TRANSCRIPT RECEIVED ===")
        logger.info(f"{content}")
        logger.info(f"=== END TRANSCRIPT ===")
        
        # Build the user message
        user_message = f"""Convert the following Photoshop tutorial into ActionJSON.

Tutorial Source: {source}
Tutorial Type: {source_type}

Tutorial Transcript:
{content}

## MANDATORY STEPS (You MUST follow these in order):

**IMPORTANT: Use relative paths (no leading slash)**

1. **FIRST - READ THE INDEX**: 
   ```
   read_file atomic_actions/index.md
   ```
   This index lists ALL available operations with their exact file paths.

2. **SECOND - IDENTIFY OPERATIONS**: Based on the transcript, identify which operations are needed and find their exact file paths from the index:
   - "duplicate layer" → `layer_management/duplicate_layer.md`
   - "select subject" → `selection/select_subject.md`
   - "add mask" → `layer_management/create_mask.md`
   - "add text" → `text_layer.md`
   - "transform/scale" → `layer_management/transform.md`
   - "convert to smart object" → `layer_management/convert_to_smart_object.md`
   - "drag layer under/over" → `layer_management/layer_reorder.md`
   - "reduce fill to 0%" → `layer_management/fill_opacity.md`
   - "stroke layer style" → `layer_management/stroke_layer_style.md`
   - "clipping mask" → `layer_management/create_clipping_mask.md`
   - "link layers" → `layer_management/link_layers.md`

3. **THIRD - READ DOCUMENTATION**: Use `read_file` to read EACH relevant .md file:
   ```
   read_file atomic_actions/layer_management/duplicate_layer.md
   read_file atomic_actions/layer_management/fill_opacity.md
   read_file atomic_actions/layer_management/stroke_layer_style.md
   ```
   
4. **FOURTH - GENERATE JSON**: ONLY after reading the docs, generate the final JSON array using the EXACT formats from the documentation.

DO NOT guess file names. Use the index to find exact paths. DO NOT skip reading documentation.

Generate the ActionJSON now by following the steps above:"""

        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Generation attempt {attempt + 1}/{max_retries}")
                
                # Log backend state before invocation
                logger.info(f"Backend cwd before invoke: {self.backend.cwd}")
                
                # Use streaming to get real-time tool call logs
                print("\n--- AGENT EXECUTION (Real-time) ---", flush=True)
                all_messages = []
                
                for event in self.agent.stream(
                    {"messages": [{"role": "user", "content": user_message}]},
                    stream_mode="updates"
                ):
                    # Log each event as it happens
                    for node_name, node_output in event.items():
                        if node_name == "tools":
                            # Tool execution
                            messages = node_output.get("messages", [])
                            for msg in messages:
                                all_messages.append(msg)
                                tool_name = getattr(msg, "name", "unknown")
                                content = str(getattr(msg, "content", ""))[:300]
                                print(f"  [TOOL RESULT] {tool_name}: {content}", flush=True)
                        elif node_name == "model":
                            # Model response
                            messages = node_output.get("messages", [])
                            for msg in messages:
                                all_messages.append(msg)
                                if hasattr(msg, "tool_calls") and msg.tool_calls:
                                    for tc in msg.tool_calls:
                                        print(f"  [TOOL CALL] {tc.get('name', 'unknown')}: {tc.get('args', {})}", flush=True)
                                elif hasattr(msg, "content") and msg.content:
                                    content_preview = str(msg.content)[:200]
                                    print(f"  [MODEL OUTPUT] {content_preview}", flush=True)
                
                print("--- END AGENT EXECUTION ---\n", flush=True)
                
                # Build result from collected messages
                result = {"messages": all_messages}
                
                logger.info(f"Backend cwd after invoke: {self.backend.cwd}")
                
                # Log all messages for debugging
                print("\n=== AGENT MESSAGES ===", flush=True)
                messages = result.get("messages", [])
                for i, msg in enumerate(messages):
                    msg_type = getattr(msg, "type", type(msg).__name__)
                    msg_content = getattr(msg, "content", str(msg))[:500] if hasattr(msg, "content") else str(msg)[:500]
                    
                    # Log tool calls if present
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        print(f"Message {i} [{msg_type}] has tool_calls:", flush=True)
                        for tc in msg.tool_calls:
                            print(f"  Tool: {tc.get('name', 'unknown')}, Args: {tc.get('args', {})}", flush=True)
                    
                    # Log tool call id if it's a tool response
                    if hasattr(msg, "tool_call_id"):
                        print(f"Message {i} [{msg_type}] tool_call_id: {msg.tool_call_id}", flush=True)
                    
                    print(f"Message {i} [{msg_type}]: {msg_content}", flush=True)
                print("=== END AGENT MESSAGES ===", flush=True)
                
                # Extract the final response
                raw_response = self._extract_final_response(result)
                logger.info(f"Agent response received, length: {len(raw_response)}")
                
                # Parse and validate the JSON
                actions, errors = self._parse_and_validate(raw_response)
                
                if actions is not None:
                    logger.info(f"Successfully generated {len(actions)} actions")
                    return {
                        "actions": actions,
                        "source": source,
                        "source_type": source_type,
                        "model": self.model_name,
                        "generator": "agent",
                        "validation_errors": errors,
                        "raw_response": raw_response,
                        "attempt": attempt + 1
                    }
                else:
                    last_error = f"Validation failed: {', '.join(errors)}"
                    logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                    
            except Exception as e:
                last_error = f"Agent error: {str(e)}"
                logger.error(f"Attempt {attempt + 1} error: {last_error}")
        
        # All retries failed
        error_msg = (
            f"Agent failed to generate valid actions after {max_retries} attempts. "
            f"Last error: {last_error}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    def _extract_final_response(self, result: Dict[str, Any]) -> str:
        """
        Extract the final text response from agent result.
        
        Args:
            result: Agent invocation result
            
        Returns:
            Final text response
        """
        messages = result.get("messages", [])
        
        # Find the last AI message
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content:
                # Skip tool call messages
                if hasattr(msg, "type") and msg.type == "tool":
                    continue
                return msg.content
            elif isinstance(msg, dict) and msg.get("content"):
                if msg.get("type") == "tool":
                    continue
                return msg["content"]
        
        return ""
    
    def _parse_and_validate(self, response: str) -> tuple[Optional[List], List[str]]:
        """
        Parse and validate the agent response.
        
        Args:
            response: Raw agent response
            
        Returns:
            Tuple of (parsed_actions or None, list_of_errors)
        """
        # Try to extract JSON from response
        json_str = self._extract_json(response)
        
        if not json_str:
            return None, ["Could not extract JSON from agent response"]
        
        try:
            data = json.loads(json_str)
            
            # Validate it's a list
            if not isinstance(data, list):
                return None, ["Response is not a JSON array"]
            
            # Basic validation of actions
            errors = []
            for i, action in enumerate(data):
                if not isinstance(action, dict):
                    errors.append(f"Action {i} is not an object")
                elif "_obj" not in action:
                    errors.append(f"Action {i} missing '_obj' field")
            
            return data, errors
            
        except json.JSONDecodeError as e:
            return None, [f"Invalid JSON: {str(e)}"]
    
    def _extract_json(self, text: str) -> Optional[str]:
        """
        Extract JSON array from text (may be wrapped in markdown code blocks).
        
        Args:
            text: Text potentially containing JSON
            
        Returns:
            Extracted JSON string or None
        """
        text = text.strip()
        
        # Try to find JSON in code blocks first
        code_block_pattern = r'```(?:json)?\s*(\[.*?\])\s*```'
        match = re.search(code_block_pattern, text, re.DOTALL)
        if match:
            return match.group(1)
        
        # Try to find JSON array directly
        array_pattern = r'(\[.*\])'
        match = re.search(array_pattern, text, re.DOTALL)
        if match:
            json_candidate = match.group(1)
            try:
                json.loads(json_candidate)
                return json_candidate
            except:
                pass
        
        # If text itself looks like JSON, return it
        if text.startswith('[') and text.endswith(']'):
            return text
        
        return None
    
    def estimate_cost(self, content_length: int) -> Dict[str, float]:
        """
        Estimate API cost for processing content.
        
        Note: Agent costs are harder to estimate due to dynamic tool usage.
        This provides a rough estimate.
        
        Args:
            content_length: Length of content in characters
            
        Returns:
            Dictionary with estimated costs
        """
        # Rough token estimate
        # Agent may make multiple calls, so we estimate higher
        base_tokens = content_length // 4
        system_tokens = len(AGENT_SYSTEM_PROMPT) // 4
        
        # Estimate agent will read ~5 doc files on average
        doc_read_tokens = 5 * 500  # ~500 tokens per doc
        
        input_tokens = base_tokens + system_tokens + doc_read_tokens
        output_tokens = 2000  # Estimate for final output
        
        # GPT-4o pricing
        input_cost_per_1k = 0.005
        output_cost_per_1k = 0.015
        
        estimated_input_cost = (input_tokens / 1000) * input_cost_per_1k
        estimated_output_cost = (output_tokens / 1000) * output_cost_per_1k
        total_cost = estimated_input_cost + estimated_output_cost
        
        return {
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "estimated_input_cost": estimated_input_cost,
            "estimated_output_cost": estimated_output_cost,
            "estimated_total_cost": total_cost,
            "currency": "USD",
            "note": "Agent costs may vary due to dynamic tool usage"
        }

