from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0005_driver_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("ACTIVE", "Active"), ("INACTIVE", "Inactive")],
                max_length=255,
                null=True,
                verbose_name="status",
            ),
        ),
    ]
