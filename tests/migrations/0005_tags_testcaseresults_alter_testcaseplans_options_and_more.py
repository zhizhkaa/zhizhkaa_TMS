# Generated by Django 4.1.7 on 2023-04-03 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0004_testplans_testcaseplans'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='TestCaseResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testCaseResult_name', models.CharField(max_length=50, verbose_name='Результат')),
            ],
            options={
                'verbose_name': 'Результат теста',
                'verbose_name_plural': 'Результаты тестов',
            },
        ),
        migrations.AlterModelOptions(
            name='testcaseplans',
            options={'verbose_name': 'Тест-кейс плана', 'verbose_name_plural': 'Тест-кейсы плана'},
        ),
        migrations.CreateModel(
            name='TestCaseTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.tags', verbose_name='Тег')),
                ('testCase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tests.testcases', verbose_name='Тест-кейс')),
            ],
            options={
                'verbose_name': 'Тег тест-кейса',
                'verbose_name_plural': 'Теги тест-кейов',
            },
        ),
        migrations.AddField(
            model_name='testcaseplans',
            name='testCaseResult',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='tests.testcaseresults', verbose_name=''),
            preserve_default=False,
        ),
    ]
