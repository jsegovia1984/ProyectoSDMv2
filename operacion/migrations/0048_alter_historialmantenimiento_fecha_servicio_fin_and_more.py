# Generated by Django 5.1.4 on 2025-02-02 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacion', '0047_remove_historialmantenimiento_fecha_ultimo_servicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialmantenimiento',
            name='fecha_servicio_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historialmantenimiento',
            name='km_servicio',
            field=models.PositiveIntegerField(),
        ),
    ]
