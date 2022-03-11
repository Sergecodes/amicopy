from django.db import models


class DeviceQueryset(models.query.QuerySet):
    def delete(self):
        # Override delete method to manually delete all objects
        for obj in self:
            obj.delete()


class DeviceManager(models.Manager):
    def get_queryset(self):
        return DeviceQueryset(self.model, using=self._db)

