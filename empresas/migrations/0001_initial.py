# Generated by Django 2.0.2 on 2018-03-19 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=30, unique=True)),
                ('nombre', models.CharField(max_length=200, unique=True)),
            ],
        ),
    ]