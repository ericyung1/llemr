# Generated by Django 3.1.2 on 2021-01-18 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_verbose_names_20210118_1141'),
        ('followup', '0004_verbose_names_20210118_1141'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccine', '0003_auto_20201209_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='comments',
            field=models.TextField(verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='completion_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vaccine_vaccineactionitem_completed', to=settings.AUTH_USER_MODEL, verbose_name='completion author'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='completion date'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='due_date',
            field=models.DateField(help_text='MM/DD/YYYY', verbose_name='due date'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='instruction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.actioninstruction', verbose_name='instruction'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='vaccineactionitem',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='vaccinedose',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='vaccinedose',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='vaccinedose',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='vaccinedose',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='vaccinedose',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='contact_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.contactmethod', verbose_name='Contact method'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='contact_resolution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='followup.contactresult', verbose_name='Contact resolution'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='vaccinefollowup',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='vaccineseries',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='vaccineseries',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='vaccineseries',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='vaccineseries',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='vaccineseries',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
    ]