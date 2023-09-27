from django.core.exceptions import ValidationError
import json

def validate_json_format(json_data):
    if not isinstance(json_data, list):
        raise ValidationError('This field must be a list.')
    
    if len(json_data) < 1:
        raise ValidationError('This list must contain at least one item.')
    
    for item in json_data:
        if not isinstance(item, dict):
            raise ValidationError('Each item in list must be a dictionary.')
        
        if not 0 < len(item.keys()) < 3:
            raise ValidationError('Each item in list must contain one or two keys ("height", "width").')
        
        for key in item.keys():
            if key not in ['height', 'width']:
                raise ValidationError('Each item in list must only contain keys "height" or "width".')
            
            if not isinstance(item[key], int):
                raise ValidationError('Each value in item must be an integer.')
            
            if item[key] < 1:
                raise ValidationError('Each value in item must be greater than 0.')
            


