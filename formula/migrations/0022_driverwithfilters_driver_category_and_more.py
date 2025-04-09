from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0021_driver_conditional_field_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverWithFilters',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('formula.driver',),
        ),
        migrations.AddField(
            model_name='driver',
            name='category',
            field=models.CharField(blank=True, choices=[('ROOKIE', 'Rookie'), ('EXPERIENCED', 'Experienced'), ('VETERAN', 'Veteran'), ('CHAMPION', 'Champion')], max_length=255, null=True, verbose_name='category'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='category',
            field=models.CharField(blank=True, choices=[('ROOKIE', 'Rookie'), ('EXPERIENCED', 'Experienced'), ('VETERAN', 'Veteran'), ('CHAMPION', 'Champion')], max_length=255, null=True, verbose_name='category'),
        ),
    ]
