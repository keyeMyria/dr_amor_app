# Generated by Django 2.0.2 on 2018-03-13 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terceros_acompanantes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoriaacompanante',
            options={'permissions': [['list_categoriaacompanante', 'Puede listar categorias acompanantes'], ['detail_categoriaacompanante', 'Puede ver detalles categoria acompanante']]},
        ),
    ]