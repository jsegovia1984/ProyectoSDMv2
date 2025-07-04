
from django.db import models

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


class Automovil(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    kilometraje = models.PositiveIntegerField()
    numero_chasis = models.CharField(max_length=30, unique=True)
    numero_motor = models.CharField(max_length=30, unique=True)
    patente = models.CharField(max_length=10, unique=True)
    vtv = models.ForeignKey(VtvEstado, on_delete=models.RESTRICT)
    visibilidad = models.BooleanField(default=True)  # Campo de visibilidad para ocultar automóviles eliminados



    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

# Create your models here.
    class Meta:
        verbose_name_plural = "Automóviles"



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


    
class ClienteParticular(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.PositiveBigIntegerField(unique=True)
    cuil = models.PositiveBigIntegerField(unique=True)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50,default="")
    email = models.EmailField(blank=True)
    visible = models.BooleanField(default=True)  # Campo de visibilidad
 
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name_plural = "Cliente particular"
    
class ClienteEmpresa(models.Model):
    nombre = models.CharField(max_length=50)
    cuit = models.PositiveBigIntegerField(unique=True)
    direccion = models.CharField(max_length=50)
    telefono = models.PositiveIntegerField(default=0)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        verbose_name_plural = "Cliente empresa"
    
