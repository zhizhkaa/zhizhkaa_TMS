# Generated by Django 4.1.7 on 2023-05-09 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0012_alter_testcaseplans_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcasesteps',
            name='testCase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.testcases', verbose_name='Тест-кейс'),
        ),
    ]
