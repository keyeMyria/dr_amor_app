# Generated by Django 2.0.2 on 2018-07-17 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basedisponibledenominacion',
            name='tipo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='efectivoentregadenominacion',
            name='tipo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
