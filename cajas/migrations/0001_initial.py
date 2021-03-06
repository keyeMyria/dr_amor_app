# Generated by Django 2.0.2 on 2018-07-17 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servicios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liquidaciones', '0001_initial'),
        ('puntos_venta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArqueoCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('dolares', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dolares_tasa', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_tarjeta', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('nro_voucher', models.PositiveIntegerField(default=0)),
                ('punto_venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bases_disponibles', to='puntos_venta.PuntoVenta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bases_disponibles_entregadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseDisponibleDenominacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('valor', models.DecimalField(decimal_places=0, max_digits=10)),
                ('arqueo_caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='base_dia_siguiente', to='cajas.ArqueoCaja')),
            ],
        ),
        migrations.CreateModel(
            name='BilleteMoneda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField()),
                ('valor', models.DecimalField(decimal_places=0, max_digits=10)),
                ('activo', models.BooleanField()),
            ],
            options={
                'permissions': [['list_billetemoneda', 'Puede listar Billetes Monedas']],
            },
        ),
        migrations.CreateModel(
            name='EfectivoEntregaDenominacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('valor', models.DecimalField(decimal_places=0, max_digits=10)),
                ('arqueo_caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entrega_efectivo', to='cajas.ArqueoCaja')),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoDineroPDV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('concepto', models.TextField()),
                ('tipo', models.CharField(blank=True, choices=[('I', 'Ingreso'), ('E', 'Egreso')], max_length=3, null=True)),
                ('tipo_dos', models.CharField(blank=True, choices=[('SER_ACOM', 'Venta Servicios'), ('CAM_TIE_SER_ACOM', 'Cambio Tiempo Servicio Acompañanate'), ('CAM_HABITACION', 'Cambio de Habitacion Servicio'), ('LIQ_ACOM', 'Liquidacion Acompañante'), ('ANU_SER_ACOM', 'Anulacion Servicio Acompañante')], max_length=30, null=True)),
                ('valor_efectivo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_tarjeta', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('franquicia', models.CharField(max_length=30, null=True)),
                ('nro_autorizacion', models.CharField(max_length=30, null=True)),
                ('arqueo_caja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimientos_dinero', to='cajas.ArqueoCaja')),
                ('creado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('liquidacion', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimientos_dinero', to='liquidaciones.LiquidacionCuenta')),
                ('punto_venta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movimientos_dinero', to='puntos_venta.PuntoVenta')),
                ('servicios', models.ManyToManyField(related_name='movimientos_dinero', to='servicios.Servicio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='billetemoneda',
            unique_together={('valor', 'tipo')},
        ),
    ]
