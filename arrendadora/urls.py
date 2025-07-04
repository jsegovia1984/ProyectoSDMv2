from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler404

# Redirigir errores 404 a la vista de advertencia

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de inicio de sesión


    # Otras URLs de tu proyecto

def redirect_to_home(request):
    return redirect('login')  # Cambia 'inicio' por el nombre de tu URL de destino


urlpatterns = [
    path('', redirect_to_home),  # Redirige la raíz a otra página
    path('admin/', admin.site.urls),
    path('operacion/', include('operacion.urls')),
    path('logout/', logout_view, name='logout'),  # Correctly reference the logout view function



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

admin.site.site_header = "SDM administración"
admin.site.site_title = "SOLUCIONES DE MOVILIDAD SA"
admin.site.index_title = "Bienvenido al panel de administración de SDM"