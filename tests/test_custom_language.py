from gesiel.messages import Messages, Config, EnglishLanguage

import pytest

from gesiel import Schema, fields
from gesiel.exceptions import InvalidSchema



def test_language():

    c = Config({Messages.MISSING_REQUIRED_FIELD: 'Campo obrigatório'})

    class Person(Schema):
        name = fields.String(required=True)

    with pytest.raises(InvalidSchema, match='Campo obrigatório') as e:
        Person.from_dict({})

    c.language = EnglishLanguage
    with pytest.raises(InvalidSchema, match='Missing required field') as e:
        Person.from_dict({})