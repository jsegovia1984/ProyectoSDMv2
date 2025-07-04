

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError



class EstadoAutomovil(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelos")

    def __str__(self):
        return f"{self.nombre} - {self.marca.nombre}"
    
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
        return f"{self.estado}"

    class Meta:
        verbose_name_plural = "VTV"


    ########################################################################################################


class Titular(models.Model):
    razon_social = models.CharField(max_length=255, blank=True, null=True, verbose_name="Razón Social")  # Razón social para personas jurídicas
    cuit = models.CharField(max_length=13, unique=True)  # CUIT/CUIL único
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    

    def __str__(self):
        return f"{self.razon_social}"
      


class Seguro(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")

    def __str__(self):
        return f"{self.nombre}"
    
class Coberturas(models.Model):
    tipo = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.tipo}"
    class Meta:
        verbose_name_plural = "Coberturas"
        
    
class Cliente(models.Model):
    razon_social = models.CharField(max_length=50, verbose_name="Razón Social")
    dni = models.PositiveBigIntegerField(unique=True, verbose_name="D.N.I.", null=True, blank=True)
    cuil = models.PositiveBigIntegerField(unique=True,null=True, blank=True, verbose_name="C.U.I.L.")
    cuit = models.PositiveBigIntegerField(unique=True,null=True, blank=True, verbose_name="C.U.I.T.")
    direccion = models.CharField(max_length=50, verbose_name="Dirección", null=True, blank=True)
    telefono = models.PositiveIntegerField(default=0, verbose_name="Teléfono")
    email = models.CharField(max_length=50, verbose_name="E-mail", null=True, blank=True)
    visible = models.BooleanField(default=True)  # Campo de visibilidad

    def __str__(self):
        return f"{self.razon_social}"
    
    class Meta:
        verbose_name_plural = "Cliente empresa"

  
class Flota(models.Model):
    descripcion = models.CharField(max_length=1500, verbose_name="Descripción")
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    disponible = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        verbose_name_plural = "Flotas"




    
class Automovil(models.Model):
    marca = models.ForeignKey('Modelo', on_delete=models.RESTRICT, blank=False, null=False)
    Estado = models.ForeignKey(EstadoAutomovil, on_delete=models.RESTRICT, blank=True, null=True)
    anio = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    kilometraje = models.PositiveIntegerField()
    numero_chasis = models.CharField(max_length=30, verbose_name="Nº de Chasis", unique=True)
    numero_motor = models.CharField(max_length=30, verbose_name="Nº de Motor", unique=True)
    patente = models.CharField(max_length=10, unique=True)
    vtv = models.ForeignKey(Vtv, on_delete=models.RESTRICT)
    poliza = models.ForeignKey('PolizaSeguro',verbose_name="Póliza", on_delete=models.RESTRICT, blank=True, null=True)
    visibilidad = models.BooleanField(default=True)  # Campo de visibilidad para ocultar automóviles eliminados
    flota = models.ForeignKey(Flota, on_delete=models.RESTRICT, blank=True, null=True)
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE, related_name='titular',null=True, blank=True)
    fecha_ultimo_servicio = models.DateField(blank=True, null=True)  # Fecha del último servicio
    km_ultimo_servicio = models.PositiveIntegerField(blank=True, null=True)  # Kilometraje del último servicio
    fecha_ultimo_siniestro = models.DateTimeField(blank=True, null=True)
    cantidad_de_sinistros = models.PositiveIntegerField(default=0)




    def __str__(self):
        return f"{self.marca} ({self.patente})"
    

    def save(self, *args, **kwargs):
        self.patente = self.patente.upper()
        super().save(*args, **kwargs)

# Create your models here.
    class Meta:
        verbose_name_plural = "Automóviles"



class Turno_VTV(models.Model):
    auto = models.ForeignKey(Automovil, on_delete=models.CASCADE, related_name="turnos")
    fecha_turno = models.DateTimeField(verbose_name="Fecha del Turno")
    lugar_verificacion = models.CharField(max_length=255, verbose_name="Lugar de Verificación")
    comentarios = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=50, 
        choices=[
            ('pendiente', 'Pendiente'),
            ('completado', 'Completado'),
            ('cancelado', 'Cancelado')
        ], 
        default='pendiente')
    



class Mantenimiento(models.Model):
    automovil = models.ForeignKey(Automovil, on_delete=models.CASCADE, related_name='mantenimientos')
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_inicio_mantenimiento = models.DateField(null=True, blank=True)
    fecha_fin_mantenimiento = models.DateField(null=True, blank=True)
    kilometraje = models.IntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    proximo_mantenimiento = models.DateField(null=True, blank=True, verbose_name="Próximo mantenimiento")
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
    direccion = models.CharField(max_length=150, verbose_name="Dirección de la aseguradora", blank=True, null=True)

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
    numero_poliza = models.CharField(max_length=50, verbose_name="Nº de póliza")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio de la póliza")
    fecha_fin = models.DateField(verbose_name="Fecha de vencimiento de la póliza")
    cobertura = models.ForeignKey(Coberturas, on_delete=models.RESTRICT, verbose_name="Cobertura de la póliza")
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


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del servicio (ej: "Cambio de aceite")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")  # Descripción opcional del servicio

    def __str__(self):
        return self.nombre
    

class HistorialMantenimiento(models.Model):
    vehiculo = models.ForeignKey(Automovil, on_delete=models.CASCADE, related_name='historial', verbose_name="Vehículo")  # Relación con el vehículo
    servicio_realizado = models.ForeignKey(Servicio, on_delete=models.RESTRICT)  # Servicio realizado
    fecha_servicio_inicio = models.DateField(blank=False, null=False)  # Fecha del último servicio
    fecha_servicio_fin = models.DateField(blank=True, null=True)  # Fecha del último servicio
    km_servicio = models.PositiveIntegerField(blank=False, null=False)  # Kilometraje del último servicio
    costo_servicio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Costo del servicio
    detalle = models.TextField(blank=True, null=True)  # Detalle del servicio
    comentarios = models.TextField(blank=True, null=True)  # Comentarios adicionales

    def clean(self):
        """
        Valida que el kilometraje ingresado sea mayor que el último registrado para el automóvil.
        """
        try:
            ultimo_mantenimiento = HistorialMantenimiento.objects.filter(vehiculo=self.vehiculo).latest('fecha_servicio_inicio')
        except HistorialMantenimiento.DoesNotExist:
            ultimo_mantenimiento = None  # Si no hay registros, se asigna None

        if ultimo_mantenimiento:
            if self.km_servicio <= ultimo_mantenimiento.km_servicio:
                raise ValidationError(
                    f"El kilometraje debe ser mayor que el último registrado: {ultimo_mantenimiento.km_servicio} km."
                )
        
        print(self.vehiculo.patente)
        auto = Automovil.objects.get(patente=self.vehiculo.patente)

        if ultimo_mantenimiento == None:
           auto.kilometraje = self.km_servicio
        else:
            auto.kilometraje = ultimo_mantenimiento.km_servicio
        
        auto.save()

    def save(self, *args, **kwargs):
        """
        Llama a clean() antes de guardar para asegurar la validación.
        """
        self.clean()
        super().save(*args, **kwargs)



    def __str__(self):
        return f"Historial de {self.vehiculo} - Último servicio: {self.fecha_servicio_inicio}"


    
class TipoSiniestro(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre
    
class Siniestro(models.Model):
    vehiculo = models.ForeignKey(Automovil, on_delete=models.CASCADE, related_name="siniestros", verbose_name="Vehículo")
    tipo = models.ForeignKey(TipoSiniestro, on_delete=models.CASCADE, related_name="siniestros")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha = models.DateField(blank=False, null=False, verbose_name="Fecha del siniestro")
    ubicacion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ubicación")
    severidad_daños = models.CharField(max_length=10, choices=[('leve', 'Leve'), ('moderado', 'Moderado'), ('severo', 'Severo')])
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cobertura_seguro = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo.nombre} - {self.vehiculo} ({self.fecha.strftime('%Y-%m-%d')})"
    


class Infracciones(models.Model):
    auto = models.ForeignKey(Automovil, on_delete=models.CASCADE, verbose_name="Auto asociado", related_name="actas")
    numero = models.CharField(max_length=20, unique=True, verbose_name="Nº de acta")
    fecha = models.DateTimeField(verbose_name="Fecha y Hora del acta")
    infraccion = models.TextField(verbose_name="Descripción de la infracción")
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto de la multa")
    puntos_descontar = models.IntegerField(default=0, verbose_name="Puntos a descontar")
    puntos_reasignar = models.IntegerField(default=0, verbose_name="Puntos a reasignar")
    lugar = models.CharField(max_length=255, verbose_name="Lugar de la infracción")
    estado = models.TextField(verbose_name="Estado del acta")
    legajo = models.CharField(max_length=20, verbose_name="Nº de legajo")

   #foto = models.ImageField(upload_to='actas/', null=True, blank=True, verbose_name="Foto de la infracción")

    def __str__(self):
        return f"Acta {self.numero} - {self.fecha}"
    

class Contrato(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    auto = models.ForeignKey('Automovil', on_delete=models.CASCADE, blank=True, null=True)
    flota = models.ForeignKey('Flota', on_delete=models.CASCADE, blank=True, null=True)
    contrato_firmado = models.BooleanField(default=False)
    fecha_contrato_firmado = models.DateField(null=True, blank=True)
    facturacion = models.BooleanField(default=False, verbose_name="Facturación")

    def __str__(self):
        return f"Contrato de {self.cliente} - {self.auto}"



    
class notas(models.Model):
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha = models.DateTimeField(verbose_name="Fecha y Hora de la nota")
    prioridad = models.CharField(max_length=50,
        choices=[
            ('baja', 'Baja'),
            ('media', 'Media'),
            ('alta', 'Alta')],
        default='media')
    titulo = models.CharField(max_length=255, verbose_name="Título de la nota")