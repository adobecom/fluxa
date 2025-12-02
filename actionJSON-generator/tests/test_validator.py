"""
Tests for validation utilities
"""

import pytest
from fluxa.utils.validator import ActionValidator, validate_json


class TestActionValidator:
    """Test ActionValidator class"""
    
    def test_valid_emboss_action(self):
        """Test validation of valid emboss action"""
        validator = ActionValidator()
        actions = [
            {"_obj": "emboss", "amount": 100, "angle": 135, "height": 3}
        ]
        is_valid, errors = validator.validate(actions)
        assert is_valid
        assert len(errors) == 0
    
    def test_invalid_not_array(self):
        """Test validation fails for non-array"""
        validator = ActionValidator()
        is_valid, errors = validator.validate({"_obj": "emboss"})
        assert not is_valid
        assert "must be an array" in errors[0].lower()
    
    def test_empty_array(self):
        """Test validation fails for empty array"""
        validator = ActionValidator()
        is_valid, errors = validator.validate([])
        assert not is_valid
        assert "empty" in errors[0].lower()
    
    def test_missing_obj_field(self):
        """Test validation fails for missing _obj field"""
        validator = ActionValidator()
        actions = [{"amount": 100}]
        is_valid, errors = validator.validate(actions)
        assert not is_valid
        assert "_obj" in errors[0]
    
    def test_emboss_out_of_range(self):
        """Test validation warns for out-of-range emboss parameters"""
        validator = ActionValidator()
        actions = [
            {"_obj": "emboss", "amount": 1000, "angle": 500, "height": 200}
        ]
        is_valid, errors = validator.validate(actions)
        assert not is_valid
        assert len(errors) == 3  # All three parameters out of range
    
    def test_valid_open_action(self):
        """Test validation of valid open action"""
        validator = ActionValidator()
        actions = [
            {
                "_obj": "open",
                "null": {"_kind": "local", "_path": "/path/to/file.jpg"},
                "template": False
            }
        ]
        is_valid, errors = validator.validate(actions)
        assert is_valid
    
    def test_open_missing_fields(self):
        """Test validation fails for open action missing required fields"""
        validator = ActionValidator()
        actions = [{"_obj": "open"}]
        is_valid, errors = validator.validate(actions)
        assert not is_valid
        assert any("null" in err for err in errors)


def test_validate_json_function():
    """Test convenience validate_json function"""
    actions = [{"_obj": "emboss", "amount": 100, "angle": 135, "height": 3}]
    is_valid, errors = validate_json(actions)
    assert is_valid
    assert len(errors) == 0


