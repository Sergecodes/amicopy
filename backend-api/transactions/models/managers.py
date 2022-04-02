from django.db import models


class DeviceQueryset(models.query.QuerySet):
    def delete(self, really_delete=False):
        # Override delete method to loop through queryset and manually delete objects
        for obj in self:
            obj.delete(really_delete)


class DeviceManager(models.Manager):
    def get_queryset(self):
        return DeviceQueryset(self.model, using=self._db)

