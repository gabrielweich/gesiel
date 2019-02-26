import pytest

from gesiel import Schema
from gesiel.fields import Int
from gesiel.exceptions import ValidationError

def test_custom_field():
    class Code(Int):
        def load(self, value):
            code = super(Code, self).load(value)
            return code*2

    class Person(Schema):
        code = Code()

    assert Person.from_dict({'code': "25"}).code == 50

def test_single_field():
    assert Int().load('2') == 2
    with pytest.raises(ValidationError):
        Int().load('gesiel')
        
def test_single_custom_field():
    class Code(Int):
        def load(self, value):
            code = super(Code, self).load(value)
            return code*2
    
    assert Code().load('2') == 4