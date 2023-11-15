import re
from pydantic import BaseModel, ValidationError, EmailStr
from datetime import datetime


class Model(BaseModel):
    email: EmailStr


def check_date(value: str) -> bool:
    """ Проверка соответствия формату DD.MM.YYYY или YYYY-MM-DD"""
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False


def check_phone(value: str) -> bool:
    """ Проверка соответствия формату +7 xxx xxx xx xx"""
    pattern = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
    result = bool(re.match(pattern, value))
    if result:
        return True
    else:
        return False


def check_email(value: str) -> bool:
    """ Проверяет является поле email или нет """
    try:
        Model(email=value)
        return True
    except ValidationError:
        return False


def data_convert(value: dict) -> dict:
    """"""
    for key in value:
        if check_date(value[key]):
            value[key] = 'date'
        elif check_phone(value[key]):
            value[key] = 'phone'
        elif check_email(value[key]):
            value[key] = 'email'
        else:
            value[key] = 'text'
    return value
