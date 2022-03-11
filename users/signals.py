# from django.contrib.auth import get_user_model
# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from django.utils.translation import gettext_lazy as _

# User = get_user_model()


# @receiver(pre_delete, sender=User)
# def deactivate_user(sender, instance: User, **kwargs):
#     really_delete = kwargs.pop('really_delete', False)

#     if not really_delete:
#         instance.deactivate()

