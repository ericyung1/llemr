# Generated by Django 3.1.2 on 2021-01-18 18:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_verbose_name_20210118_1256'),
        ('labs', '0004_auto_20201209_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='continuousmeasurementtype',
            name='lab_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='labs.labtype', verbose_name='lab type'),
        ),
        migrations.AlterField(
            model_name='continuousmeasurementtype',
            name='order_index',
            field=models.PositiveIntegerField(default=0, help_text='Order at which this measurement will display', verbose_name='order index'),
        ),
        migrations.AlterField(
            model_name='discretemeasurementtype',
            name='lab_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='labs.labtype', verbose_name='lab type'),
        ),
        migrations.AlterField(
            model_name='discretemeasurementtype',
            name='order_index',
            field=models.PositiveIntegerField(default=0, help_text='Order at which this measurement will display', verbose_name='order index'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='lab_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='lab time'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='lab_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='labs.labtype', verbose_name='lab type'),
        ),
        migrations.AlterField(
            model_name='lab',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='labtype',
            name='order_index',
            field=models.PositiveIntegerField(default=0, verbose_name='order index'),
        ),
    ]
