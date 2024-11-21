from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0019_circuit_created_at_circuit_modified_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="race",
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
