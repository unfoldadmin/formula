from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import formula.encoders
import simple_history.models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0008_alter_driver_options_alter_driver_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalDriver",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=255, verbose_name="last name"),
                ),
                (
                    "picture",
                    models.TextField(
                        blank=True,
                        default=None,
                        max_length=100,
                        null=True,
                        verbose_name="picture",
                    ),
                ),
                ("code", models.CharField(max_length=3, verbose_name="code")),
                (
                    "color",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="color"
                    ),
                ),
                (
                    "salary_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("EUR", "Euro"), ("USD", "US Dollar")],
                        default=None,
                        editable=False,
                        max_length=3,
                        null=True,
                    ),
                ),
                (
                    "salary",
                    djmoney.models.fields.MoneyField(
                        blank=True, decimal_places=2, max_digits=14, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")],
                        max_length=255,
                        null=True,
                        verbose_name="status",
                    ),
                ),
                (
                    "data",
                    models.JSONField(
                        blank=True,
                        encoder=formula.encoders.PrettyJSONEncoder,
                        null=True,
                        verbose_name="data",
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical driver",
                "verbose_name_plural": "historical drivers",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
