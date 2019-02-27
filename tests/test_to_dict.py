import pytest

from gesiel import fields, Schema

def test_assign():
    class Person(Schema):
        name = fields.String()
    
    p = Person.from_dict({'name': "gesiel"})

    assert Person.to_dict(p)['name'] == "gesiel"
    p.name = 'manuel'
    assert p.name == 'manuel'
    assert Person.to_dict(p)['name'] == "manuel"


def test_to_dict_with_none():
    class Person(Schema):
        name = fields.String()
    
    assert Person.from_dict({'name': None}).to_dict()['name'] is None

def test_to_dict_with_none():
    class Person(Schema):
        name = fields.String()
    
    assert 'name' not in Person.from_dict({'name': None}).to_dict(skip_none=True)


def test_skip_load():
    class Person(Schema):
        code = fields.String()
    
    assert Person.from_dict({'code': 25}, skip_load=True).code == 25


def test_nest():
    class Person(Schema):
        name = fields.String(default="Gesiel")
        age = fields.Int(required=True)
        dead = fields.Bool()
        color = fields.String()
    assert Person.from_dict(Person.from_dict({'age': 25, 'dead': None}).to_dict()).to_dict(skip_none=True) == {'age': 25, 'name':'Gesiel'}


def test_nest_with_skip_none():
    class Person(Schema):
        name = fields.String(default="Gesiel")
        age = fields.Int(required=True)
        dead = fields.Bool()
        color = fields.String()
    assert Person.from_dict(Person.from_dict({'age': 25, 'dead': None}, skip_none=True).to_dict()).to_dict(skip_none=True) == {'age': 25, 'name':'Gesiel'}