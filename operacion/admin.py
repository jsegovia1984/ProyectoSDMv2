from django.contrib import admin
from .models import Automovil,Seguro, ClienteParticular, ClienteEmpresa, Vtv, Coberturas, Poliza, VtvEstado



class SeguroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')

class CoberturasAdmin(admin.ModelAdmin):
    pass
    
class PolizaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cobertura', 'franquicia')

class ClienteParticularAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'cuil', 'direccion', 'telefono', 'email')
    search_fields = ('apellido', 'dni', 'cuil')
    list_filter = ('apellido', 'dni', 'cuil')

class ClienteEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre','cuit', 'direccion', 'telefono', 'email')
    search_fields = ('nombre','cuit')
    list_filter = ('nombre','cuit')

class AutomovilAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'kilometraje', 'numero_chasis', 'numero_motor', 'patente','vtv')
    search_fields = ('marca', 'modelo', 'numero_chasis', 'numero_motor')
    list_filter = ('marca', 'anio', 'color')
    actions = ['vtv']


    def vtv(self, request, queryset):
        pass
    vtv.short_description = "Actualizar Datos de VTV"



class VtvAdmin(admin.ModelAdmin):
    list_display = ('vencimiento','estado','turno')
    search_fields = ('vencimiento', 'estado')
    list_filter = ('vencimiento', 'estado')
   

class VtvEstadoAdmin(admin.ModelAdmin):
    list_display = ('id','estado')


admin.site.register(Automovil, AutomovilAdmin)
admin.site.register(Poliza, PolizaAdmin)
admin.site.register(Coberturas, CoberturasAdmin)
admin.site.register(Seguro, SeguroAdmin)
admin.site.register(ClienteParticular, ClienteParticularAdmin)
admin.site.register(ClienteEmpresa, ClienteEmpresaAdmin)
admin.site.register(Vtv,VtvAdmin)
admin.site.register(VtvEstado,VtvEstadoAdmin)

# Register your models here.
