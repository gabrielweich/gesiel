import pytest

from gesiel import fields, Schema
from gesiel.exceptions import InvalidSchema
from datetime import datetime, date

def test_simple_person():
    class Person(Schema):
        name = fields.String()
        age = fields.Int()
        dead = fields.Bool()
        pool = fields.Bool()

    p = Person.from_dict({'name': 'Gesiel', 'age': 29, 'dead': False})
    assert p.name == 'Gesiel'
    assert p.age == 29
    assert p.dead == False
    assert p.pool is None


def test_default():
    class Person(Schema):
        dead = fields.Bool(default=True)

    p = Person.from_dict({})
    assert p.dead == True

def test_required():
    class Person(Schema):
        name = fields.String(required=True)
    
    with pytest.raises(InvalidSchema, match='Missing required field'):
        Person.from_dict({})

def test_none():
    class Person(Schema):
        name = fields.String()
    
    p = Person.from_dict({'name': None})
    assert p.name is None


def test_pass_none():
    class Person(Schema):
        name = fields.String(required=True)
    
    p = Person.from_dict({'name': None})
    assert p.name is None

def test_pass_none_with_skip_none():
    class Person(Schema):
        name = fields.String(required=True)
        age = fields.Int()

    p = Person.from_dict({'name': None, 'age':23})
    assert p.to_dict() == {'name': None, 'age': 23}
    assert p.to_dict(skip_none=True) == {'age': 23}

    with pytest.raises(InvalidSchema, match='Missing required field'):
        Person.from_dict({'name': None}, skip_none=True)


def test_pass_none_with_default():
    class Person(Schema):
        name = fields.String(default='Gesiel')
    
    p = Person.from_dict({'name': None})
    assert p.name is None


def test_pass_none_with_default_and_skip():
    class Person(Schema):
        name = fields.String(required=True, default='Gesiel')
    
    p = Person.from_dict({'name': None}, skip_none=True)
    assert p.name == 'Gesiel'


def test_post_load():
    class Phone(Schema):
        ddd = fields.String()
        number = fields.String()

        def post_load(self, context):
            if context['number'][:2] == context['ddd']:
                context['number'] = context['number'][2:]
            return context

    
    assert Phone.from_dict({'number': '55991484554', 'ddd':55}).number == '991484554'


def test_post_load_update():
    class Phone(Schema):
        name = fields.String()

        def post_load(self, context):
            context['name'] = context['name'].upper()
            return context

    
    assert Phone.from_dict({'name': 'gesiel'}).name == 'GESIEL'


def test_post_load_new_field():
    class Phone(Schema):
        name = fields.String()
        lastname = fields.String()

        def post_load(self, context):
            context['full_name'] = context['name'] + " " + context['lastname']
            return context

    
    assert Phone.from_dict({'name': 'Gesiel', 'lastname': 'Souza'}).full_name == 'Gesiel Souza'


def test_method():
    class Person(Schema):
        name = fields.String()

        def say_name(self):
            return f'Hi, I am {self.name}'

    assert Person.from_dict({'name':'Gesiel'}).say_name() == "Hi, I am Gesiel"

def test_set_self_attr():
    class Person(Schema):
        def init(self):
            self.name = 'Gesiel'

    p = Person.from_dict({})
    p.init()
    assert p.to_dict() == {'name': 'Gesiel'}

def test_number():
    class Person(Schema):
        salary = fields.Number()
    
    assert Person.from_dict({'salary': 200.15}).salary == 200.15
    assert isinstance(Person.from_dict({'salary': 200}).salary, float)


