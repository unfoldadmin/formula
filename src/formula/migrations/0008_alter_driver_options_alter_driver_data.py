from django.db import migrations, models
import formula.encoders


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0007_driver_data"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="driver",
            options={
                "permissions": (("update_statistics", "Update statistics"),),
                "verbose_name": "driver",
                "verbose_name_plural": "drivers",
            },
        ),
        migrations.AlterField(
            model_name="driver",
            name="data",
            field=models.JSONField(
                blank=True,
                encoder=formula.encoders.PrettyJSONEncoder,
                null=True,
                verbose_name="data",
            ),
        ),
    ]
