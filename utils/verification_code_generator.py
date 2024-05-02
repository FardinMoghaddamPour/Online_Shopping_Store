import random
import string


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))
