from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0006_driver_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="data",
            field=models.JSONField(blank=True, null=True, verbose_name="data"),
        ),
    ]
