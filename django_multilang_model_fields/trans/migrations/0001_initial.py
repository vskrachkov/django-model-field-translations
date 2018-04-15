# Generated by Django 2.0.4 on 2018-04-15 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('full_name', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('main_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation', related_query_name='translation', to='trans.Content')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
