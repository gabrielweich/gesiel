import pytest

from gesiel import fields, Schema



def test_merge_simple():
    class Person(Schema):
        name = fields.String()
        last_name = fields.String()
        age = fields.Int()
        dead = fields.Bool()

    assert Person.from_dict({'name': None, 'age': 20,  'last_name': None}).merge({'age': 35, 'last_name': 'Souza'}).to_dict(skip_none=True) == {'age': 35, 'last_name': 'Souza'}


def test_merge_with_skip_none():
    class Person(Schema):
        name = fields.String()
        last_name = fields.String()
        age = fields.Int()
        dead = fields.Bool(default=False)

    assert Person.from_dict({'name': None, 'age': 20,  'last_name': None}).merge({'age': 35, 'last_name': 'Souza', 'dead': None}, skip_none=True).to_dict() == {'name': None, 'age': 35, 'last_name': 'Souza', 'dead': False}
