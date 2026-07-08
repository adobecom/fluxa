"""
AI-powered Photoshop Action JSON generator
"""

import json
import re
from typing import Dict, Any, List, Optional
from openai import OpenAI
from ..prompts.photoshop_actions import (
    get_system_prompt,
    get_user_prompt,
    get_few_shot_examples
)
from ..utils.validator import validate_json_string


class PhotoshopActionGenerator:
    """Generate Photoshop API JSON from tutorial content using OpenAI"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5.1",
        temperature: float = 0.1,
        max_tokens: int = 4000,
        timeout: int = 60
    ):
        """
        Initialize the generator
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-5.1)
            temperature: Generation temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
        """
        self.client = OpenAI(api_key=api_key, timeout=timeout)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(
        self,
        content: str,
        source: str,
        source_type: str,
        use_few_shot: bool = True,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Generate Photoshop actions from tutorial content
        
        Args:
            content: Tutorial text content
            source: Source URL
            source_type: Type of source (youtube or web)
            use_few_shot: Whether to include few-shot examples
            max_retries: Maximum retry attempts for failed generations
            
        Returns:
            Dictionary with generated actions and metadata
            
        Raises:
            ValueError: If generation fails after retries
        """
        # Build messages
        messages = [
            {"role": "system", "content": get_system_prompt()}
        ]
        
        # Add few-shot examples if requested
        if use_few_shot:
            messages.extend(get_few_shot_examples())
        
        # Add user prompt
        user_prompt = get_user_prompt(content, source, source_type)
        messages.append({"role": "user", "content": user_prompt})
        
        # Try generation with retries
        last_error = None
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                # Extract response content
                raw_response = response.choices[0].message.content
                
                # Parse and validate
                actions, errors = self._parse_and_validate(raw_response)
                
                if actions is not None:
                    return {
                        "actions": actions,
                        "source": source,
                        "source_type": source_type,
                        "model": self.model,
                        "validation_errors": errors,
                        "raw_response": raw_response,
                        "attempt": attempt + 1
                    }
                else:
                    last_error = f"Validation failed: {', '.join(errors)}"
                    
            except Exception as e:
                last_error = f"API error: {str(e)}"
        
        # All retries failed
        raise ValueError(
            f"Failed to generate valid actions after {max_retries} attempts. "
            f"Last error: {last_error}"
        )
    
    def _parse_and_validate(self, response: str) -> tuple[Optional[List], List[str]]:
        """
        Parse and validate the AI response
        
        Args:
            response: Raw AI response
            
        Returns:
            Tuple of (parsed_actions or None, list_of_errors)
        """
        # Try to extract JSON from response
        json_str = self._extract_json(response)
        
        if not json_str:
            return None, ["Could not extract JSON from response"]
        
        # Validate JSON
        is_valid, errors, data = validate_json_string(json_str)
        
        if is_valid:
            return data, []
        else:
            # Return data even with validation errors (might still be usable)
            return data if data is not None else None, errors
    
    def _extract_json(self, text: str) -> Optional[str]:
        """
        Extract JSON array from text (may be wrapped in markdown code blocks)
        
        Args:
            text: Text potentially containing JSON
            
        Returns:
            Extracted JSON string or None
        """
        # Remove markdown code blocks if present
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
            # Quick validation that it looks like JSON
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
        Estimate API cost for processing content
        
        Args:
            content_length: Length of content in characters
            
        Returns:
            Dictionary with estimated costs
        """
        # Rough token estimate (1 token ≈ 4 characters)
        input_tokens = (len(get_system_prompt()) + content_length) // 4
        output_tokens = self.max_tokens
        
        # GPT-4o pricing (as of 2024)
        # These are approximate and should be updated
        input_cost_per_1k = 0.005  # $5 per 1M tokens
        output_cost_per_1k = 0.015  # $15 per 1M tokens
        
        estimated_input_cost = (input_tokens / 1000) * input_cost_per_1k
        estimated_output_cost = (output_tokens / 1000) * output_cost_per_1k
        total_cost = estimated_input_cost + estimated_output_cost
        
        return {
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "estimated_input_cost": estimated_input_cost,
            "estimated_output_cost": estimated_output_cost,
            "estimated_total_cost": total_cost,
            "currency": "USD"
        }


