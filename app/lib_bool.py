
import uuid

def is_int(text):
    try:
        int(text)
        return True
    except:
        return False

def is_float(text):
    try:
        float(text)
        return True
    except:
        return False


def create_token():
    lowercase_str = uuid.uuid4().hex
    return str(lowercase_str)
