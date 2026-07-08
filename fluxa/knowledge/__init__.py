"""
Knowledge base for Photoshop operations
"""

import json
import os
from typing import Dict, Any


def load_operations() -> Dict[str, Any]:
    """Load Photoshop operations knowledge base"""
    current_dir = os.path.dirname(__file__)
    json_path = os.path.join(current_dir, 'photoshop_operations.json')
    
    with open(json_path, 'r') as f:
        return json.load(f)


__all__ = ["load_operations"]


