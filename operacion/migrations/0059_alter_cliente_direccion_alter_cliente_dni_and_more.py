# Generated by Django 5.1.3 on 2025-02-12 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0058_alter_automovil_numero_chasis_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(max_length=50, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.PositiveBigIntegerField(unique=True, verbose_name='D.N.I.'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(max_length=50, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='razon_social',
            field=models.CharField(max_length=50, verbose_name='Razón Social'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.PositiveIntegerField(default=0, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='flota',
            name='descripcion',
            field=models.CharField(max_length=50, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='historialmantenimiento',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='operacion.automovil', verbose_name='Vehículo'),
        ),
        migrations.AlterField(
            model_name='infracciones',
            name='fecha',
            field=models.DateTimeField(verbose_name='Fecha y Hora del acta'),
        ),
        migrations.AlterField(
            model_name='infracciones',
            name='legajo',
            field=models.CharField(max_length=20, verbose_name='Nº de legajo'),
        ),
        migrations.AlterField(
            model_name='infracciones',
            name='numero',
            field=models.CharField(max_length=20, unique=True, verbose_name='Nº de acta'),
        ),
        migrations.AlterField(
            model_name='polizaseguro',
            name='numero_poliza',
            field=models.CharField(max_length=50, verbose_name='Nº de póliza'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='siniestro',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='siniestro',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ubicación'),
        ),
        migrations.AlterField(
            model_name='siniestro',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='siniestros', to='operacion.automovil', verbose_name='Vehículo'),
        ),
        migrations.AlterField(
            model_name='tiposiniestro',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='turno_vtv',
            name='fecha_turno',
            field=models.DateTimeField(verbose_name='Fecha del Turno'),
        ),
        migrations.AlterField(
            model_name='turno_vtv',
            name='lugar_verificacion',
            field=models.CharField(max_length=255, verbose_name='Lugar de Verificación'),
        ),
    ]
