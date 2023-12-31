from django.core.exceptions import ValidationError


def validate_json_format(json_data):
    if not isinstance(json_data, list):
        raise ValidationError('This field must be a list.')
    
    if len(json_data) < 1:
        raise ValidationError('This list must contain at least one item.')
    
    for item in json_data:
        if not isinstance(item, dict):
            raise ValidationError('Each item in list must be a dictionary.')
        
        if len(item.keys()) != 1:
            raise ValidationError('Each item in list must contain only one key "height" or "width").')
        
        key = list(item.keys())[0]

        if key not in ['height', 'width']:
            raise ValidationError('Each item in list must only contain keys "height" or "width".')
        
        if not isinstance(item[key], int):
            raise ValidationError('Each value in item must be an integer.')
        
        if item[key] < 1:
            raise ValidationError('Each value in item must be greater than 0.')
            


