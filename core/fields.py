from django.db import models


class ProperEmailField(models.EmailField):
    description = "An email field that replaces @googlemail.com to @gmail.com since both are actually the same"
   
    def _parse_value(self, value: str):
        # Domain part of email should already be in lowercase since email is normalized
        # before saving
        return value.replace('@googlemail.com', '@gmail.com')

    def get_db_prep_value(self, value, *args, **kwargs):
        if value is None:
            return None
        return self._parse_value(str(value))

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return self._parse_value(str(value))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)



