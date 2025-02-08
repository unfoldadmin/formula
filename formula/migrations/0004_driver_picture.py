from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0003_driver_constructors"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="picture",
            field=models.ImageField(
                blank=True,
                default=None,
                null=True,
                upload_to="",
                verbose_name="picture",
            ),
        ),
    ]
