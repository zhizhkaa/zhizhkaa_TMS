# Generated by Django 4.1.7 on 2023-05-01 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_alter_testcases_suite'),
    ]

    operations = [
        migrations.AddField(
            model_name='testplans',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tests.projects', verbose_name='Проект'),
            preserve_default=False,
        ),
    ]
