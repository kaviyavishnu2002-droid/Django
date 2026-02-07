import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def __call__(self, value):
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Must contain uppercase letter")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Must contain number")
        if not re.search(r'[@$!%*#?&]', value):
            raise ValidationError("Must contain special character")

class Min_Length:
    def __init__(self, min_length, message = None):
        self.min_length = min_length
        self.message = message or f"minimum length should be {min_length}"

    def __call__(self, value):
        if value is None:
            value = ''
        if len(str(value)) < self.min_length:
            raise ValidationError(self.message)

def No_Numbers(value):
    if any(val.isdigit() for val in value):
        raise ValidationError("number are not allowed in this field")
    
def over18(value):
    if value <= 18:
        raise ValidationError("should be 18 pluse in this field")
    
def within18(value):
    if value >= 18:
        raise ValidationError("should be within 18 in this field")
    
def only18(value):
    if value != 18:
        raise ValidationError("only allowed must 18 in this field")

class Min_Length_Validator:
    def __init__(self, min_length, message=None):
        self.min_length = min_length
        self.message = message or f"Minimum length is {min_length}"

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, Min_Length_Validator)
            and self.min_length == other.min_length
        )
