# Generated by Django 2.0.2 on 2018-03-19 20:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('terceros', '0007_auto_20180319_1635'),
        ('inventarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoInventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fecha', models.DateField()),
                ('comprobante_numero', models.CharField(max_length=20)),
                ('detalle', models.TextField()),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movimientos', to='inventarios.Bodega')),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimientos_inventarios', to='terceros.Tercero')),
            ],
            options={
                'permissions': [['list_movimientoinventario', 'Puede listar movimientos inventario'], ['detail_movimientoinventario', 'Puede ver detalle movimientos inventario']],
            },
        ),
        migrations.CreateModel(
            name='MovimientoInventarioDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('costo_unitario', models.DecimalField(decimal_places=2, max_digits=12)),
                ('entra_cantidad', models.DecimalField(decimal_places=2, max_digits=12)),
                ('entra_costo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('sale_cantidad', models.DecimalField(decimal_places=2, max_digits=12)),
                ('sale_costo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('saldo_cantidad', models.DecimalField(decimal_places=2, max_digits=12)),
                ('saldo_costo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('movimiento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='detalles', to='inventarios.MovimientoInventario')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]