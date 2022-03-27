from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class UserQuerySet(QuerySet):
    def delete(self, really_delete=False):
        if really_delete:
            return super().delete()
        else:
            self.deactivate()

    def deactivate(self):
        self.update(is_active=False, deactivated_on=timezone.now())


class UserManager(BaseUserManager):
    # Override this to enable logging with djoser via username and/or email 
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

