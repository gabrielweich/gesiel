from .fields import Field
from .exceptions import ValidationError, InvalidSchema
from .messages import Messages
from collections import defaultdict
import inspect
import json

class SchemaCreator(type):
    def __new__(mcs, *args, **kwargs):
        args[2]['_fields'] = list(filter(lambda f: isinstance(f[1], Field) and not f[0].startswith('_'), args[2].items()))
        return type.__new__(mcs, *args)


class Schema(metaclass=SchemaCreator):
    @classmethod
    def from_dict(cls, values, skip_none=False, skip_load=False, skip_validate=False):
        errors = defaultdict(list)
        field_values = {}
        instance = cls()

        for name, field in cls._fields:
            if name in values and values[name] is not None:
                if skip_load:
                    field_values[name] = values[name]
                else:
                    try:
                        value = field.load(values[name])
                        validation_errors = []
                        if not skip_validate:
                            validation_errors = field.validate(value)
                        if validation_errors:
                            errors[name].extend(validation_errors)
                        else:
                            field_values[name] = value
                    except ValidationError as error:
                        errors[name].append(error)
            elif name not in values or (skip_none and values[name] is None):
                if field.default is not None:
                    field_values[name] = field.default
                elif field.required:
                    errors[name].append(ValidationError(error_code=Messages.MISSING_REQUIRED_FIELD))
            elif values[name] is None:
                field_values[name] = None
        if errors:
            raise InvalidSchema(errors)
        
        post_context = cls.post_load(instance, field_values)

        for key, value in post_context.items():
            setattr(instance, key, value)

        return instance

    def post_load(self, context):
        return context

    def to_dict(self, skip_none=False):
        attributes = self.__dict__

        if skip_none:
            return {k:v for k,v in attributes.items() if v is not None}
        return attributes
    
    def merge(self, values, skip_none=False):
        if skip_none:
            for k, v in values.items():
                if v is not None and hasattr(self, k):
                    setattr(self, k, v)
        else:
            for k, v in values.items():
                if hasattr(self, k):
                    setattr(self, k, v)

        return self

    def __str__(self):
        return json.dumps(self.to_dict(skip_none=True))