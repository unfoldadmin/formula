from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from formula.exceptions import ReadonlyException


@receiver(pre_save)
def update_timestamp(sender, instance, **kwargs):
    if not settings.DEBUG and sender._meta.db_table != "studio_options":
        raise ReadonlyException(
            "Database is operating in readonly mode. Not possible to save any data."
        )
