import secrets
import string

class PasswordGenerator:
    def __init__(self, length=8):
        self.length = length
        self.alphabet = string.ascii_letters + string.digits

    def generate_password(self):
        while True:
            password = ''.join(secrets.choice(self.alphabet) for i in range(self.length))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
                return password