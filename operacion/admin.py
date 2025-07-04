from django.contrib import admin
from .models import  Coberturas, VtvEstado,Marca,Modelo,TipoSiniestro,EstadoAutomovil


class EstadoAutomovilAdmin(admin.ModelAdmin):
    pass

class MarcaAdmin(admin.ModelAdmin):
    pass

class ModeloAdmin(admin.ModelAdmin):
    pass

class CoberturasAdmin(admin.ModelAdmin):
    pass
    
class VtvEstadoAdmin(admin.ModelAdmin):
    pass

class TipoSiniestroAdmin(admin.ModelAdmin):
    pass


admin.site.register(Coberturas, CoberturasAdmin)
admin.site.register(VtvEstado,VtvEstadoAdmin)
admin.site.register(Marca,MarcaAdmin)
admin.site.register(Modelo,ModeloAdmin)
admin.site.register(TipoSiniestro,TipoSiniestroAdmin)
admin.site.register(EstadoAutomovil,EstadoAutomovilAdmin)
# Register your models here.
