from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0004_driver_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="color",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="color"
            ),
        ),
    ]
