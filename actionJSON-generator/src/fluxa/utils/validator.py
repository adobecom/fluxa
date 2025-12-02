"""
JSON validation utilities for Photoshop API actions
"""

from typing import List, Dict, Any, Tuple
import json


class ActionValidator:
    """Validator for Photoshop API action JSON"""
    
    def __init__(self):
        """Initialize validator with known operations"""
        self.known_operations = {
            # Basic operations
            'emboss', 'open', 'save', 'close', 'make', 'delete', 'select',
            'show', 'hide', 'set', 'move', 'fill', 'reset', 'exchange',
            'duplicate', 'merge', 'flatten', 'crop', 'resize', 'rotate',
            'transform', 'apply', 'copy', 'paste', 'cut',
            # Adjustments
            'desaturate', 'invert', 'brightnessEvent', 'hueSaturation',
            'vibrance', 'levels', 'curves', 'colorBalance', 'photoFilter',
            'blackAndWhite', 'exposure', 'posterize', 'threshold',
            # Filters
            'gaussianBlur', 'motionBlur', 'radialBlur', 'surfaceBlur',
            'addNoise', 'unsharpMask', 'highPass', 'differenceClouds',
            'tiltShift', 'minimum', 'maximum',
            # Selection
            'autoCutout', 'inverse', 'colorRange', 'modifySelection',
            # Layer operations
            'mergeVisible', 'mergeLayersNew', 'newPlacedLayer', 'placeEvent',
            'layerSection', 'contentAwareFill',
            # Other
            'Adobe Camera Raw Filter'
        }
    
    def validate(self, data: Any) -> Tuple[bool, List[str]]:
        """
        Validate Photoshop API action JSON
        
        Args:
            data: Parsed JSON data
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if it's a list
        if not isinstance(data, list):
            errors.append("Root element must be an array of actions")
            return False, errors
        
        # Check if empty
        if len(data) == 0:
            errors.append("Action array is empty")
            return False, errors
        
        # Validate each action
        for idx, action in enumerate(data):
            action_errors = self._validate_action(action, idx)
            errors.extend(action_errors)
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _validate_action(self, action: Any, idx: int) -> List[str]:
        """Validate a single action object"""
        errors = []
        
        # Must be an object/dict
        if not isinstance(action, dict):
            errors.append(f"Action at index {idx} is not an object")
            return errors
        
        # Must have _obj field
        if '_obj' not in action:
            errors.append(f"Action at index {idx} missing required '_obj' field")
            return errors
        
        obj_type = action['_obj']
        
        # Warn about unknown operations
        if obj_type not in self.known_operations:
            errors.append(
                f"Action at index {idx}: '{obj_type}' is not a recognized operation "
                f"(this may still be valid)"
            )
        
        # Validate specific operation types
        if obj_type == 'emboss':
            errors.extend(self._validate_emboss(action, idx))
        elif obj_type == 'open':
            errors.extend(self._validate_open(action, idx))
        elif obj_type == 'save':
            errors.extend(self._validate_save(action, idx))
        
        return errors
    
    def _validate_emboss(self, action: Dict[str, Any], idx: int) -> List[str]:
        """Validate emboss action"""
        errors = []
        
        if 'amount' in action:
            amount = action['amount']
            if not isinstance(amount, (int, float)) or not (1 <= amount <= 500):
                errors.append(
                    f"Action at index {idx}: emboss 'amount' should be between 1 and 500"
                )
        
        if 'angle' in action:
            angle = action['angle']
            if not isinstance(angle, (int, float)) or not (-360 <= angle <= 360):
                errors.append(
                    f"Action at index {idx}: emboss 'angle' should be between -360 and 360"
                )
        
        if 'height' in action:
            height = action['height']
            if not isinstance(height, (int, float)) or not (1 <= height <= 100):
                errors.append(
                    f"Action at index {idx}: emboss 'height' should be between 1 and 100"
                )
        
        return errors
    
    def _validate_open(self, action: Dict[str, Any], idx: int) -> List[str]:
        """Validate open action"""
        errors = []
        
        if 'null' not in action:
            errors.append(f"Action at index {idx}: 'open' action missing 'null' field")
        elif isinstance(action['null'], dict):
            null_obj = action['null']
            if '_kind' not in null_obj:
                errors.append(
                    f"Action at index {idx}: 'open' action 'null' missing '_kind' field"
                )
            if '_path' not in null_obj:
                errors.append(
                    f"Action at index {idx}: 'open' action 'null' missing '_path' field"
                )
        
        return errors
    
    def _validate_save(self, action: Dict[str, Any], idx: int) -> List[str]:
        """Validate save action"""
        errors = []
        
        if 'in' not in action:
            errors.append(f"Action at index {idx}: 'save' action missing 'in' field")
        elif isinstance(action['in'], dict):
            in_obj = action['in']
            if '_kind' not in in_obj:
                errors.append(
                    f"Action at index {idx}: 'save' action 'in' missing '_kind' field"
                )
            if '_path' not in in_obj:
                errors.append(
                    f"Action at index {idx}: 'save' action 'in' missing '_path' field"
                )
        
        return errors


def validate_json(json_data: Any) -> Tuple[bool, List[str]]:
    """
    Convenience function to validate Photoshop API JSON
    
    Args:
        json_data: Parsed JSON data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    validator = ActionValidator()
    return validator.validate(json_data)


def validate_json_string(json_string: str) -> Tuple[bool, List[str], Any]:
    """
    Validate JSON string
    
    Args:
        json_string: JSON string to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors, parsed_data)
    """
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {str(e)}"], None
    
    is_valid, errors = validate_json(data)
    return is_valid, errors, data


