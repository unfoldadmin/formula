import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0026_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='circuit',
            options={'ordering': ['weight'], 'verbose_name': 'circuit', 'verbose_name_plural': 'circuits'},
        ),
        migrations.AlterModelOptions(
            name='constructor',
            options={'ordering': ['weight'], 'verbose_name': 'constructor', 'verbose_name_plural': 'constructors'},
        ),
        migrations.AddField(
            model_name='circuit',
            name='weight',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='weight'),
        ),
        migrations.AddField(
            model_name='constructor',
            name='weight',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='weight'),
        ),
        migrations.AlterField(
            model_name='standing',
            name='points',
            field=models.DecimalField(decimal_places=2, help_text='Points scored by the driver/constructor in the race', max_digits=4, verbose_name='points'),
        ),
        migrations.CreateModel(
            name='PitStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('time', models.TimeField(verbose_name='time')),
                ('duration', models.TimeField(verbose_name='duration')),
                ('lap', models.PositiveIntegerField(verbose_name='lap')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='formula.driver', verbose_name='driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='formula.race', verbose_name='race')),
            ],
            options={
                'verbose_name': 'pit stop',
                'verbose_name_plural': 'pit stops',
                'db_table': 'pit_stops',
            },
        ),
    ]
