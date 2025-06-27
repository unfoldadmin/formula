from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0024_driver_standing_historicaldriver_standing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='is_retired',
            field=models.BooleanField(choices=[(None, ''), (True, 'Active'), (False, 'Inactive')], null=True, verbose_name='retired'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='is_retired',
            field=models.BooleanField(choices=[(None, ''), (True, 'Active'), (False, 'Inactive')], null=True, verbose_name='retired'),
        ),
        migrations.AddField(
            model_name='historicaldriverwithfilters',
            name='is_retired',
            field=models.BooleanField(choices=[(None, ''), (True, 'Active'), (False, 'Inactive')], null=True, verbose_name='retired'),
        ),
    ]
