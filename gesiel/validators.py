from .exceptions import ValidationError
from .messages import Messages
import math
import re


class Length:
    def __init__(self, min: int=0, max: int=math.inf):
        self.min = min
        self.max = max

    def __call__(self, value):
        size = len(value)
        if size < self.min:
            raise ValidationError(error_code=Messages.MINIMUM_LENGTH, minimum_value=self.min)
        if size > self.max:
            raise ValidationError(error_code=Messages.MAXIMUM_LENGTH, maximum_value=self.max)


class Email:
    def __call__(self, value):
        if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', value):
            raise ValidationError(error_code=Messages.MUST_BE_EMAIL)