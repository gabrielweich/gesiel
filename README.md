# Gesiel - Simple and Flexible Schema Definition



Gesiel allows the definition of powerful schemas in python.

  - No dependencies.
  - Plain python objects.
  - It works.


### Simple Usage
```python
from gesiel import fields, Schema
from gesiel.validators import Length, Email

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
```



### Custom fields
```python
class Code(Int):
    def load(self, value):
        code = super(Code, self).load(value)
        return code*2

class Person(Schema):
    code = Code()

assert Person.from_dict({'code': "25"}).code == 50
```

### Validators
```python
from gesiel.exceptions import InvalidSchema, ValidationError

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
```



### Skip None
```python
class Person(Schema):
    name = fields.String(required=True)
    age = fields.Int()

p = Person.from_dict({'name': None, 'age':23})
assert p.to_dict() == {'name': None, 'age': 23}
assert p.to_dict(skip_none=True) == {'age': 23}

with pytest.raises(InvalidSchema, match='Missing required field'):
    Person.from_dict({'name': None}, skip_none=True)
```


### Post load
```python
class Person(Schema):
    name = fields.String()
    lastname = fields.String()

    def post_load(self, context):
        context['full_name'] = context['name'] + " " + context['lastname']
        return context


assert Person.from_dict({'name': 'Gesiel', 'lastname': 'Souza'}).full_name == 'Gesiel Souza'
```


### Custom language
```python
from gesiel.messages import Messages, Config, EnglishLanguage

c = Config({Messages.MISSING_REQUIRED_FIELD: 'Campo obrigatório'})

class Person(Schema):
    name = fields.String(required=True)

with pytest.raises(InvalidSchema, match='Campo obrigatório') as e:
    Person.from_dict({})

c.language = EnglishLanguage
with pytest.raises(InvalidSchema, match='Missing required field') as e:
    Person.from_dict({})
```


### Merge
```python
class Person(Schema):
    name = fields.String()
    last_name = fields.String()
    age = fields.Int()
    dead = fields.Bool(default=False)

assert Person.from_dict({'name': None, 'age': 20,  'last_name': None}).merge({'age': 35, 'last_name': 'Souza', 'dead': None}, skip_none=True).to_dict() == {'name': None, 'age': 35, 'last_name': 'Souza', 'dead': False}

```

## Important:
 - Still in alpha.
 - Full docs are in progress.
