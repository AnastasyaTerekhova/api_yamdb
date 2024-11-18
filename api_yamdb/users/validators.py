import re

from django.forms import ValidationError


def username_validator(value):
    pattern = r'^[\w.@+-]+\Z'
    if not re.match(pattern, value['username']):
        raise ValidationError(
            ('Имя пользователя не соответствует требованиям. '
             'Имя пользователя должно содержать только буквы, '
             'цифры, и символы @/./+/-/_'),
            params={'value': value},
        )
    if value['username'] == 'me':
        raise ValidationError(('Вы не можете использовать '
                               'такое имя пользователя'),
                              params={'value': value})
    if len(value['username']) > 150:
        raise ValidationError(('Имя пользователя должно быть короче '
                               '150 сиволов'),
                              params={'value': value})
    if len(value['email']) > 150:
        raise ValidationError(('Email пользователя должен быть короче '
                               '254 сиволов'),
                              params={'value': value})


def username_pattern_validator(value):
    pattern = r'^[\w.@+-]+\Z'
    if not re.match(pattern, value):
        raise ValidationError(
            ('Имя пользователя не соответствует '
             'требованиям. Имя пользователя должно содержать '
             'только буквы, цифры, и символы @/./+/-/_'))
