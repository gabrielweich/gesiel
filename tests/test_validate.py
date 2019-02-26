import pytest

from gesiel import Schema, fields

from gesiel.validators import Length, Email
from gesiel.exceptions import InvalidSchema, ValidationError


def test_simple_validator():
    class Person(Schema):
        name = fields.String(validators=[Length(2, 6)])
    
    with pytest.raises(InvalidSchema, match='Maximum of 6 character'):
        Person.from_dict({'name': "supergesiel"})

    with pytest.raises(InvalidSchema,  match='At least 2 character'):
        Person.from_dict({'name': "g"})

    assert Person.from_dict({'name': "gesiel"}).name == "gesiel"



def test_multiple_validators():
    def validate_name(name):
        if name[0] != "f":
            raise ValidationError('Name does not starts with f')

    class Person(Schema):
        name = fields.String(validators=[Length(2, 6), validate_name])
    
    with pytest.raises(InvalidSchema):
        Person.from_dict({'name': "gesiel"})
    
    with pytest.raises(InvalidSchema):
        Person.from_dict({'name': "g"})

    assert Person.from_dict({'name': "fesiel"}).name == "fesiel"


def test_email():
    class Person(Schema):
        email = fields.String(validators=[Email()])
    
    with pytest.raises(InvalidSchema):
        Person.from_dict({'email': "gesielemail.com"})

    assert Person.from_dict({'email': "gesiel@email.com"}).email == "gesiel@email.com"


def test_home_example():
    class Person(Schema):
        name = fields.String()
        age = fields.Int(required=True)
        email = fields.String(validators=[Email()])
        dead = fields.Bool(default=False)
        description = fields.String(validators=[Length(5, 150)])

    p = Person.from_dict({'name': 'Gesiel', 'age': 29, 'email':'gesiel@email.com'})
    p.description = 'Test description'
    assert p.to_dict() == {
        'name': 'Gesiel',
        'age': 29,
        'email': 'gesiel@email.com',
        'dead': False,
        'description': 'Test description'
    }
