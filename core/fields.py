# Ref: https://docs.djangoproject.com/en/3.2/ref/models/fields/#field-api-reference

import serpy
from django.db.models import EmailField
from shortuuid.django_fields import ShortUUIDField


class ProperEmailField(EmailField):
    description = "An email field that replaces @googlemail.com to @gmail.com since both are actually the same"
   
    def _parse_value(self, value: str):
        from users.models.managers import UserManager

        value = UserManager.normalize_email(value)
        return value.replace('@googlemail.com', '@gmail.com')

    def get_prep_value(self, value):
        # When storing to db
        value = super().get_prep_value(value)
        if value is None:
            return None
        return self._parse_value(str(value))

    def to_python(self, value):
        # When displaying
        if value is None:
            return value
        return self._parse_value(str(value))

    def from_db_value(self, value, expression, connection):
        # After retrieving from db
        return self.to_python(value)


class ReadableShortUUIDField(ShortUUIDField):
    description = "A uuid field that separates given groups of characters with a separator; to ease readability"

    def __init__(self, *args, **kwargs):
        self.group_by = kwargs.pop('group_by', 4)
        self.sep = kwargs.pop('separator', '-')

        if self.group_by is None:
            raise ValueError("ReadableShortUUIDFields must define a 'group_by' attribute")

        super().__init__(*args, **kwargs)

    def _parse_value(self, value: str, sep: str, group_by: int):
        """
        Convert value like aaaabbbbcccc to aaaa-bbbb-cccc depending on `sep` and `group_by`
        """
        n = group_by
        grouped_list = [value[i:i+n] for i in range(0, len(value), n)]
        return sep.join(grouped_list)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None

        # Remove hyphens 
        return value.replace('-', '')

    def to_python(self, value):
        if value is None:
            return value
        return self._parse_value(value, self.sep, self.group_by)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)


## Custom serpy serializer fields
class SerpyDateTimeField(serpy.Field):
    def to_value(self, value):
        return None if value is None else value.isoformat()


