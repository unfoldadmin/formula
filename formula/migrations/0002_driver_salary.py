from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="salary",
            field=djmoney.models.fields.MoneyField(
                blank=True, decimal_places=2, max_digits=14, null=True
            ),
        ),
        migrations.AddField(
            model_name="driver",
            name="salary_currency",
            field=djmoney.models.fields.CurrencyField(
                choices=[("EUR", "Euro"), ("USD", "US Dollar")],
                default=None,
                editable=False,
                max_length=3,
                null=True,
            ),
        ),
    ]
