# Generated by Django 4.0.6 on 2022-10-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domains',
            fields=[
                ('uuid', models.CharField(max_length=36, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
    ]
