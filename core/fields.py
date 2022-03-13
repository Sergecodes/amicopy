from django.db.models import EmailField

from users.models.managers import UserManager


class ProperEmailField(EmailField):
    description = "An email field that replaces @googlemail.com to @gmail.com since both are actually the same"
   
    def _parse_value(self, value: str):
        value = UserManager.normalize_email(value)
        return value.replace('@googlemail.com', '@gmail.com')

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        return self._parse_value(str(value))

    def to_python(self, value):
        if value is None:
            return value
        return self._parse_value(str(value))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)



