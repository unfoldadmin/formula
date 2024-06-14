from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0011_circuit_name_de_circuit_name_en"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="resume",
            field=models.FileField(
                blank=True, default=None, null=True, upload_to="", verbose_name="resume"
            ),
        ),
        migrations.AddField(
            model_name="historicaldriver",
            name="resume",
            field=models.TextField(
                blank=True,
                default=None,
                max_length=100,
                null=True,
                verbose_name="resume",
            ),
        ),
    ]
