class Messages:
    MISSING_REQUIRED_FIELD = 1
    MUST_BE_STRING = 2
    MUST_BE_INTEGER = 3
    MUST_BE_BOOLEAN = 4
    MUST_BE_NUMBER = 5
    MUST_BE_LIST = 6
    MUST_BE_DICT = 7
    MINIMUM_LENGTH = 8
    MAXIMUM_LENGTH = 9
    MUST_BE_EMAIL = 10

EnglishLanguage = {
    Messages.MISSING_REQUIRED_FIELD: "Missing required field",
    Messages.MUST_BE_STRING: "Must be a string",
    Messages.MUST_BE_INTEGER: "Must be a valid integer",
    Messages.MUST_BE_NUMBER: "Must be a valid number",
    Messages.MUST_BE_LIST: "Must be a list",
    Messages.MUST_BE_DICT: "Must be a map",
    Messages.MINIMUM_LENGTH: "At least {minimum_value} character(s).",
    Messages.MAXIMUM_LENGTH: "Maximum of {maximum_value} character(s).",
    Messages.MUST_BE_EMAIL: 'Must be a valid email address',
}


class Config(object):
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Config,cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, language=EnglishLanguage):      
        if(self.__initialized): return
        self.__initialized = True
        self.language = language

    @classmethod
    def get_language(cls):
        return cls().language

