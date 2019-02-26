import json
from .messages import Config

class ValidationError(Exception):
    def __init__(self, message='', error_code=None, **extra):
        language = Config.get_language()
        msg = message if error_code not in language else language[error_code]
        super().__init__(msg.format(**extra))


class InvalidSchema(Exception):
    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__("Invalid schema: " + json.dumps(errors, default=str, ensure_ascii=False))