import re

def valid_email(s: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s))

def non_negative_age(a: int) -> bool:
    try:
        return int(a) >= 0
    except:
        return False
