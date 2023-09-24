from django.conf import settings
from django.db.backends.signals import connection_created


def activate_foreign_keys(sender, connection, **kwargs):
    if not settings.DEBUG and connection.vendor == "sqlite":
        cursor = connection.cursor()
        cursor.execute("PRAGMA query_only = ON;")


connection_created.connect(activate_foreign_keys)
