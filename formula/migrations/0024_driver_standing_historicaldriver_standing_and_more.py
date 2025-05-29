import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula', '0023_driver_best_time_driver_born_at_driver_editor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='standing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='standing', to='formula.standing', verbose_name='standing'),
        ),
        migrations.AddField(
            model_name='historicaldriver',
            name='standing',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formula.standing', verbose_name='standing'),
        ),
        migrations.AddField(
            model_name='historicaldriverwithfilters',
            name='standing',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='formula.standing', verbose_name='standing'),
        ),
        migrations.AlterField(
            model_name='standing',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='standings', to='formula.driver', verbose_name='driver'),
        ),
    ]
