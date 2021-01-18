# Generated by Django 3.1.2 on 2021-01-18 17:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_verbose_names_20210118_1141'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workup', '0007_auto_20201203_1940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workup',
            options={'ordering': ['-encounter__clinic_day'], 'permissions': [('export_pdf_Workup', 'Can export note PDF'), ('sign_Workup', 'Can sign note')]},
        ),
        migrations.RemoveField(
            model_name='historicalworkup',
            name='clinic_day',
        ),
        migrations.RemoveField(
            model_name='historicalworkup',
            name='will_return',
        ),
        migrations.RemoveField(
            model_name='workup',
            name='clinic_day',
        ),
        migrations.RemoveField(
            model_name='workup',
            name='referral_location',
        ),
        migrations.RemoveField(
            model_name='workup',
            name='referral_type',
        ),
        migrations.RemoveField(
            model_name='workup',
            name='will_return',
        ),
        migrations.AlterField(
            model_name='addendum',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='addendum',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='addendum',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='addendum',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='addendum',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='attestablebasicnote',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='attestablebasicnote',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='attestablebasicnote',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='attestablebasicnote',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='attestablebasicnote',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='basicnote',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='basicnote',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='basicnote',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='basicnote',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='basicnote',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='historicalattestablebasicnote',
            name='author',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='historicalattestablebasicnote',
            name='author_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='historicalattestablebasicnote',
            name='last_modified',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='historicalattestablebasicnote',
            name='patient',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='historicalattestablebasicnote',
            name='written_datetime',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='historicalbasicnote',
            name='author',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='historicalbasicnote',
            name='author_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='historicalbasicnote',
            name='last_modified',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='historicalbasicnote',
            name='patient',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='historicalbasicnote',
            name='written_datetime',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='author',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='author_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='encounter',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.encounter', verbose_name='Encounter'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='got_voucher',
            field=models.BooleanField(default=False, verbose_name='Got voucher'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='imaging_voucher_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Imaging voucher'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='last_modified',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='patient',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='patient_pays',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Patient pays'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='patient_pays_imaging',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Patient pays imaging'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='voucher_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Voucher amount'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='historicalworkup',
            name='written_datetime',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='written_datetime'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='author_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.group', verbose_name='author type'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='encounter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.encounter', verbose_name='Encounter'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='got_voucher',
            field=models.BooleanField(default=False, verbose_name='Got voucher'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Height'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='imaging_voucher_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Imaging voucher'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.patient', verbose_name='patient'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='patient_pays',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Patient pays'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='patient_pays_imaging',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Patient pays imaging'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='voucher_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Voucher amount'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Weight'),
        ),
        migrations.AlterField(
            model_name='workup',
            name='written_datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='written_datetime'),
        ),
        migrations.DeleteModel(
            name='ClinicDate',
        ),
        migrations.DeleteModel(
            name='ClinicType',
        ),
    ]