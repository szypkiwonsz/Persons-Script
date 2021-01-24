class Password:
    """Class representing Password object."""

    def __init__(self, password):
        self.password = password
        self.rating = 0

    def __str__(self):
        return f'Password: {self.password}, rating: {self.rating}'


class PasswordRater(Password):
    """Inheriting class storing methods for rating password."""

    def rate_password(self):
        """Rates password by the guidelines."""
        self.check_for_digit()
        self.check_length()
        self.check_uppercase()
        self.check_lowercase()
        self.check_special_character()

    def increase_password_rating(self, number):
        self.rating += number

    def check_lowercase(self):
        if any(c.islower() for c in self.password):
            self.increase_password_rating(1)

    def check_uppercase(self):
        if any(c.isupper() for c in self.password):
            self.increase_password_rating(2)

    def check_for_digit(self):
        if any(c.isdigit() for c in self.password):
            self.increase_password_rating(1)

    def check_length(self):
        if len(self.password) >= 8:
            self.increase_password_rating(5)

    def check_special_character(self):
        for c in self.password:
            if not c.isalnum():
                self.increase_password_rating(3)
                break
