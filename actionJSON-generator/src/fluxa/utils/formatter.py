"""
Output formatting utilities
"""

import json
from datetime import datetime
from typing import Any, Dict


def format_output(data: Any, indent: int = 2) -> str:
    """
    Format JSON data for output
    
    Args:
        data: JSON data to format
        indent: Indentation spaces
        
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)


def add_metadata(
    data: Any,
    source: str = None,
    source_type: str = None,
    generated_at: str = None
) -> Dict[str, Any]:
    """
    Add metadata wrapper to action JSON
    
    Args:
        data: Action array
        source: Source URL
        source_type: Type of source (youtube/web)
        generated_at: Generation timestamp
        
    Returns:
        Dictionary with metadata and actions
    """
    if generated_at is None:
        generated_at = datetime.utcnow().isoformat() + "Z"
    
    result = {
        "_metadata": {
            "generated_by": "Fluxa AI Tool",
            "generated_at": generated_at,
            "version": "0.1.0"
        },
        "actions": data
    }
    
    if source:
        result["_metadata"]["source"] = source
    if source_type:
        result["_metadata"]["source_type"] = source_type
    
    return result


def strip_metadata(data: Dict[str, Any]) -> Any:
    """
    Remove metadata wrapper and return just actions
    
    Args:
        data: Dictionary possibly containing metadata
        
    Returns:
        Actions array
    """
    if isinstance(data, dict) and "actions" in data:
        return data["actions"]
    return data


