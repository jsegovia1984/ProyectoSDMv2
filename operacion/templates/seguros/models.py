

from django.db import models
from django.utils import timezone
from datetime import timedelta


class VtvEstado(models.Model):
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.estado}"
    class Meta:
        verbose_name_plural = "VTV estado"


class Vtv(models.Model):
    vencimiento = models.DateField()
    turno = models.BooleanField()
    estado = models.ForeignKey(VtvEstado, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.estado} {self.turno} {self.vencimiento}"

    class Meta:
        verbose_name_plural = "VTV"

class Titular(models.Model):
    razon_social = models.CharField(max_length=255, blank=True, null=True)  # Razón social para personas jurídicas
    cuit = models.CharField(max_length=13, unique=True)  # CUIT/CUIL único
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    

    def __str__(self):
        return f"{self.razon_social}"
      


class Seguro(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre}"
    
class Coberturas(models.Model):
    tipo = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.tipo}"
    class Meta:
        verbose_name_plural = "Coberturas"
        
class Poliza(models.Model):
    empresa = models.ForeignKey(Seguro, on_delete=models.RESTRICT)
    cobertura = models.ForeignKey(Coberturas, on_delete=models.RESTRICT)
    franquicia = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.empresa} {self.cobertura}"

    
class Cliente(models.Model):
    razon_social = models.CharField(max_length=50)
    dni = models.PositiveBigIntegerField(unique=True)
    cuil = models.PositiveBigIntegerField(unique=True)
    cuit = models.PositiveBigIntegerField(unique=True)
    direccion = models.CharField(max_length=50)
    telefono = models.PositiveIntegerField(default=0)
    email = models.CharField(max_length=50)
    visible = models.BooleanField(default=True)  # Campo de visibilidad

    def __str__(self):
        return f"{self.razon_social}"
    
    class Meta:
        verbose_name_plural = "Cliente empresa"

  
class Flota(models.Model):
    descripcion = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    disponible = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = "Flotas"


class Automovil(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    kilometraje = models.PositiveIntegerField()
    numero_chasis = models.CharField(max_length=30, unique=True)
    numero_motor = models.CharField(max_length=30, unique=True)
    patente = models.CharField(max_length=10, unique=True)
    vtv = models.ForeignKey(Vtv, on_delete=models.RESTRICT)
    visibilidad = models.BooleanField(default=True)  # Campo de visibilidad para ocultar automóviles eliminados
    flota = models.ForeignKey(Flota, on_delete=models.RESTRICT, blank=True, null=True)
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE, related_name='titular',null=True, blank=True)


    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

# Create your models here.
    class Meta:
        verbose_name_plural = "Automóviles"


class Turno_VTV(models.Model):
    auto = models.ForeignKey(Automovil, on_delete=models.CASCADE, related_name="turnos")
    fecha_turno = models.DateTimeField()
    lugar_verificacion = models.CharField(max_length=255)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, 
        choices=[
            ('pendiente', 'Pendiente'),
            ('completado', 'Completado'),
            ('cancelado', 'Cancelado')
        ], 
        default='pendiente')
    

# class Turno_VTV(models.Model):
#     auto = models.ForeignKey(Automovil, related_name='turnos', on_delete=models.CASCADE)
#     fecha_turno = models.DateTimeField()
#     lugar_verificacion = models.CharField(max_length=255)
#     estado = models.CharField(
#         max_length=50, 
#         choices=[
#             ('pendiente', 'Pendiente'),
#             ('completado', 'Completado'),
#             ('cancelado', 'Cancelado')
#         ], 
#         default='pendiente'
#     )
#     comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Turno para {self.auto.patente} en {self.fecha_turno}'


class Mantenimiento(models.Model):
    automovil = models.ForeignKey(Automovil, on_delete=models.CASCADE, related_name='mantenimientos')
    descripcion = models.TextField()
    fecha_inicio_mantenimiento = models.DateField(null=True, blank=True)
    fecha_fin_mantenimiento = models.DateField(null=True, blank=True)
    kilometraje = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    tipo_mantenimiento = models.CharField(max_length=50, choices=[
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    ])

    def __str__(self):
        return f"Mantenimiento {self.tipo_mantenimiento} - {self.fecha_inicio_mantenimiento} - {self.automovil}"

    class Meta:
        ordering = ['fecha_inicio_mantenimiento']




class Aseguradora(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la aseguradora")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono de contacto")
    email = models.EmailField(verbose_name="Correo electrónico")
    sitio_web = models.URLField(verbose_name="Sitio web", blank=True, null=True)
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Aseguradora"
        verbose_name_plural = "Aseguradoras"

# from django.core.validators import MinValueValidator

class PolizaSeguro(models.Model):

    aseguradora = models.ForeignKey(
        Aseguradora,
        on_delete=models.CASCADE,
        verbose_name="Aseguradora",
        related_name='polizas'
    )
    numero_poliza = models.CharField(max_length=50, verbose_name="Número de póliza")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio de la póliza")
    fecha_fin = models.DateField(verbose_name="Fecha de vencimiento de la póliza")
    cobertura = models.TextField(verbose_name="Cobertura de la póliza", blank=True, null=True)
    # costo = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     verbose_name="Costo de la póliza",
    #     validators=[MinValueValidator(0)]
    # )
    activa = models.BooleanField(default=True, verbose_name="¿Póliza activa?")

    def __str__(self):
        return f"Póliza {self.numero_poliza}"

    class Meta:
        verbose_name = "Póliza de seguro"
        verbose_name_plural = "Pólizas de seguro"
