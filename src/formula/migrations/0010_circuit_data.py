from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0009_historicaldriver"),
    ]

    operations = [
        migrations.AddField(
            model_name="circuit",
            name="data",
            field=models.JSONField(blank=True, null=True, verbose_name="data"),
        ),
    ]
