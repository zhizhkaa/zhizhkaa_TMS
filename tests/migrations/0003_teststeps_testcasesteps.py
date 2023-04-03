# Generated by Django 4.1.7 on 2023-04-03 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_alter_testtypes_options_alter_testcases_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSteps',
            fields=[
                ('testStep_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Код шага')),
                ('description', models.CharField(max_length=100, verbose_name='Описание шага')),
                ('expectedResult', models.TextField(verbose_name='Ожидаемый результат')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tests.projects', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Шаги теста',
                'verbose_name_plural': 'Шаги тестов',
            },
        ),
        migrations.CreateModel(
            name='TestCaseSteps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testCaseStep_num', models.PositiveIntegerField(verbose_name='Номер шага')),
                ('testCase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tests.testcases', verbose_name='Тест-кейс')),
                ('testStep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.teststeps', verbose_name='Шаг')),
            ],
            options={
                'verbose_name': 'Шаги тест-кейса',
                'verbose_name_plural': 'Шаги тест-кейсов',
            },
        ),
    ]
