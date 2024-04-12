
import re 
import string

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False

def format_phone_number(phone_number):
    pattern = r'(\d{3})(\d{3})(\d{4})'
    formatted_number = re.sub(pattern, r'+XX-\1-\2-\3', phone_number)
    return formatted_number


def validate_name(name):
    # 이름이 빈 문자열인지 확인
    if not name:
        return False
    # 모든 문자가 알파벳 또는 공백인지 확인
    if all(char in string.ascii_letters or char in string.whitespace for char in name):
        return True
    else:
        return False
