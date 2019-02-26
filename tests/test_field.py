import pytest

from gesiel import Schema
from gesiel.fields import Int

def test_custom_field():
    class Code(Int):
        def load(self, value):
            code = super(Code, self).load(value)
            return code*2

    class Person(Schema):
        code = Code()

    assert Person.from_dict({'code': "25"}).code == 50
