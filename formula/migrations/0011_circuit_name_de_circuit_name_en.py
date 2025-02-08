from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("formula", "0010_circuit_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="circuit",
            name="name_de",
            field=models.CharField(max_length=255, null=True, verbose_name="name"),
        ),
        migrations.AddField(
            model_name="circuit",
            name="name_en",
            field=models.CharField(max_length=255, null=True, verbose_name="name"),
        ),
    ]
