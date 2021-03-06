import crypt
import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeCanvas

from model_utils.models import TimeStampedModel

from terceros_acompanantes.models import CategoriaAcompanante


class Tercero(models.Model):
    def imagen_perfil_upload_to(instance, filename):
        nro_random = random.randint(1111, 9999)
        return "img/usuarios/perfil/%s01j%sj10%s.%s" % (instance.id, nro_random, instance.id, filename.split('.')[-1])

    CHOICES_TIPO_DOCUMENTO = (
        ('CC', 'Cédula Ciudadanía'),
        ('CE', 'Cédula Extrangería'),
        ('PS', 'Pasaporte'),
        ('TI', 'Tarjeta Identidad'),
        ('NI', 'Nit'),
    )

    CHOICES_SEXO = (
        ('F', 'Femenino'),
        ('M', 'Masculino')
    )

    CHOICES_ESTADO = (
        (0, 'Disponible'),
        (1, 'Ocupado')
    )

    usuario = models.OneToOneField(User, on_delete=models.PROTECT, related_name='tercero', null=True, blank=True)
    tipo_documento = models.CharField(max_length=2, choices=CHOICES_TIPO_DOCUMENTO, default='CC')
    nro_identificacion = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=400)
    nombre_segundo = models.CharField(max_length=60, null=True, blank=True)
    apellido = models.CharField(max_length=60, null=True, blank=True)
    apellido_segundo = models.CharField(max_length=60, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(choices=CHOICES_SEXO, default='F', max_length=20, null=True, blank=True)
    grupo_sanguineo = models.CharField(max_length=60, null=True, blank=True)
    es_acompanante = models.BooleanField(default=False)
    es_colaborador = models.BooleanField(default=False)
    es_proveedor = models.BooleanField(default=False)
    presente = models.BooleanField(default=False)
    pin = models.CharField(max_length=128, null=True)
    qr_acceso = models.CharField(max_length=300, null=True)
    imagen_perfil = ProcessedImageField(
        processors=[ResizeToFit(300, 300)],
        format='PNG',
        options={'quality': 100},
        null=True,
        blank=True,
        upload_to=imagen_perfil_upload_to
    )
    # campo para acompañante
    alias_modelo = models.CharField(max_length=120, blank=True, null=True, unique=True)
    categoria_modelo = models.ForeignKey(CategoriaAcompanante, on_delete=models.PROTECT, blank=True, null=True,
                                         related_name='acompanantes')
    estado = models.PositiveIntegerField(choices=CHOICES_ESTADO, default=0)

    def set_new_pin(self, raw_pin):
        self.pin = crypt.crypt(raw_pin)
        self.save()

    def is_pin_correct(self, raw_pin):
        return crypt.crypt(raw_pin, self.pin) == self.pin

    @staticmethod
    def existe_documento(nro_identificacion: str) -> bool:
        return Tercero.objects.filter(nro_identificacion=nro_identificacion).exists()

    @staticmethod
    def existe_alias(alias: str) -> bool:
        return Tercero.objects.filter(alias_modelo=alias).exists()

    @property
    def full_name_proxy(self) -> str:
        if self.es_acompanante:
            return self.alias_modelo
        else:
            nombre_segundo = ''
            if self.nombre_segundo:
                nombre_segundo = ' %s' % (self.nombre_segundo)

            apellido = ''
            if self.apellido_segundo:
                apellido = ' %s' % (self.apellido)

            apellido_segundo = ''
            if self.apellido_segundo:
                apellido_segundo = ' %s' % (self.apellido_segundo)

            return '%s%s %s%s' % (self.nombre, nombre_segundo, apellido, apellido_segundo)

    @property
    def full_name(self) -> str:
        nombre_segundo = ''
        if self.nombre_segundo:
            nombre_segundo = ' %s' % (self.nombre_segundo)

        apellido_segundo = ''
        if self.apellido_segundo:
            apellido_segundo = ' %s' % (self.apellido_segundo)

        return '%s%s %s%s' % (self.nombre, nombre_segundo, self.apellido, apellido_segundo)

    @property
    def identificacion(self) -> str:
        return '%s %s' % (self.get_tipo_documento_display(), self.nro_identificacion)

    @property
    def cuenta_abierta_mesero(self):
        cuenta = self.usuario.cuentas.filter(liquidada=False, tipo=2).first()
        if not cuenta:
            cuenta = self.usuario.cuentas.create(liquidada=False, tipo=2)
        return cuenta

    @property
    def ultima_cuenta_mesero_liquidada(self):
        cuenta = self.usuario.cuentas.filter(liquidada=True, tipo=2).last()
        return cuenta

    @property
    def cuenta_abierta(self):
        cuenta = self.usuario.cuentas.filter(liquidada=False, tipo=1).first()
        if not cuenta:
            cuenta = self.usuario.cuentas.create(liquidada=False, tipo=1)
        return cuenta

    @property
    def ultima_cuenta_liquidada(self):
        cuenta = self.usuario.cuentas.filter(liquidada=True, tipo=1).last()
        return cuenta

    def generarQR(self):
        now = timezone.now().astimezone()
        nro_aleatorio = random.randint(1000, 9999)
        import secrets  # imports secure module.
        secure_random = secrets.SystemRandom()
        caracteres = ["a", "e", "i", "o", "u", "%", "&", "/", ")", "(", "=", "?", "¿", "{", "}", "*", "+", "¡", "!"]
        random_uno = random.randint(10, 99).__str__().join(secure_random.sample(caracteres, 3))
        random_dos = random.choice(caracteres).join(secure_random.sample(caracteres, 3))
        random_tres = random.randint(100, 999).__str__().join(secure_random.sample(caracteres, 3))

        qr_acceso = '%s%s%s%s%s%s(%s)%s$%s%s%s' % (
            self.id,
            random_uno,
            nro_aleatorio,
            random_dos,
            now.month,
            nro_aleatorio,
            self.usuario_id,
            now.year,
            random_tres,
            now.day,
            self.id,
        )
        self.qr_acceso = qr_acceso
        self.save()

    def registra_entrada(self):
        now = timezone.now().astimezone()
        self.generarQR()
        qs = self.usuario.regitros_ingresos.filter(
            created__year=now.year,
            created__month=now.month,
            created__day=now.day,
            fecha_fin__isnull=True
        )
        if not qs.exists():
            self.usuario.regitros_ingresos.create()

    def registra_salida(self):
        now = timezone.now().astimezone()
        self.qr_acceso = None
        self.save()
        qs = self.usuario.regitros_ingresos.filter(
            created__year=now.year,
            created__month=now.month,
            created__day=now.day,
            fecha_fin__isnull=True
        )
        if qs.exists():
            qs.update(fecha_fin=now)
        else:
            self.usuario.regitros_ingresos.create(fecha_fin=now)

    def cambiar_estado(self, nuevo_estado):
        mensaje = ''
        if self.estado != nuevo_estado:
            if nuevo_estado == 0:
                servicios = self.usuario.cuentas.filter(servicios__estado=1)
                if not servicios.exists():
                    self.estado = 0
                else:
                    mensaje = 'Existen servicios aún activos'
            if nuevo_estado == 1:
                if self.presente:
                    self.estado = 1
            self.save()
        return self.estado == nuevo_estado, mensaje

    class Meta:
        unique_together = [('tipo_documento', 'nro_identificacion')]
        permissions = [
            ['list_terceroacompanante', 'Puede listar acompanantes'],
            ['detail_terceroacompanante', 'Puede ver detalles acompanantes'],
            ['add_terceroacompanante', 'Puede adicionar acompanantes'],
            ['delete_terceroacompanante', 'Puede eliminar acompanantes'],
            ['change_terceroacompanante', 'Puede cambiar acompanantes'],
            ['list_tercerocolaborador', 'Puede listar colaboradores'],
            ['detail_tercerocolaborador', 'Puede ver detalles colaboradores'],
            ['add_tercerocolaborador', 'Puede adicionar colaboradores'],
            ['delete_tercerocolaborador', 'Puede eliminar colaboradores'],
            ['change_tercerocolaborador', 'Puede cambiar colaboradores'],
            ['list_terceroproveedor', 'Puede listar proveedores'],
            ['detail_terceroproveedor', 'Puede ver detalles proveedores'],
            ['add_terceroproveedor', 'Puede adicionar proveedores'],
            ['delete_terceroproveedor', 'Puede eliminar proveedores'],
            ['change_terceroproveedor', 'Puede cambiar proveedores'],
            ['can_be_waiter', 'Puede Ser Mesero(a)'],
        ]


class Cuenta(TimeStampedModel):
    TIPO_CHOICES = (
        (1, 'Propia'),
        (2, 'Mesero'),
    )
    propietario = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='cuentas')
    liquidada = models.BooleanField(default=False, db_index=True)
    tipo = models.PositiveIntegerField(choices=TIPO_CHOICES, default=1)
