from .models import Automovil, Cliente,VtvEstado,Turno_VTV,Flota,Titular,Aseguradora,PolizaSeguro,Servicio,HistorialMantenimiento,notas
from .models import Siniestro, Infracciones,Contrato
from .forms import InfraccionesForm
from django.shortcuts import render, redirect,get_object_or_404
from .forms import AutomovilForm
from django.contrib.auth import login, authenticate
from .forms import CustomLoginForm, ClienteForm, TurnoVTVForm, FlotaForm, TitularForm,AseguradoraForm,PolizaForm,ServicioForm,MantenimientoForm
from .forms import SiniestroForm,ContratoForm
from .utils import numero_a_letras
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import io
import datetime
import locale # Import the locale module



###########################################################################################################
# CONTRATO
###########################################################################################################

@login_required
def listado_contrato(request):
    contratos = Contrato.objects.all()
    return render(request, 'contrato/listado_contrato.html', {'contratos': contratos})

@login_required
def agregar_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_contrato')
    else:
        form = ContratoForm()    
    return render(request, 'contrato/agregar_contrato.html', {'form': form})

@login_required
def eliminar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    contrato.delete()
    return redirect('listado_contrato')

@login_required
def editar_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('listado_contrato')
    else:
        form = ContratoForm(instance=contrato)
    return render(request, 'contrato/editar_contrato.html', {'form': form})




# @login_required # Uncomment if you are using it
def generar_contrato(request, pk): # Using contrato_id as per our last discussion
    # Set the locale to Spanish for date formatting
    # The exact locale string might vary slightly by operating system:
    # 'es_ES.UTF-8' for Linux/macOS, 'es_ES' for some systems, 'Spanish_Spain.1252' for Windows
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') # Common for Linux/macOS
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES') # Alternative for some Linux/macOS
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252') # For Windows
            except locale.Error:
                # Fallback if no specific Spanish locale is found
                print("Warning: Could not set Spanish locale for date formatting.")


    contrato = get_object_or_404(Contrato, pk=pk)

    arrendador_data = {
        'razon_social': "SOLUCIONES DE MOVILIDAD S.A",
        'cuit': "30-71553750-4",
        'representante_nombre': "Pablo Hector Confenti",
        'representante_dni': "20.620.511",
        'domicilio': "Gallo N° 1651 de la Ciudad Autónoma de Buenos Aires",
    }

    context = {
        'contrato': contrato,
        'arrendador': arrendador_data,
        # Formateo de fecha para el inicio del contrato
        'dia_contrato': contrato.fecha_contrato_firmado.day if contrato.fecha_contrato_firmado else '[DIA]',
        # This will now use the Spanish locale
        'mes_contrato': contrato.fecha_contrato_firmado.strftime('%B').upper() if contrato.fecha_contrato_firmado else '[MES]',
        'anio_contrato': contrato.fecha_contrato_firmado.year if contrato.fecha_contrato_firmado else '[AÑO]',
        'monto_inicial': contrato.monto_inicial,
        'monto_letras': numero_a_letras(contrato.monto_inicial),
    }

    html_string = render_to_string('contrato/contrato.html', context) # Ensure this path is correct

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    
    filename_parts = [f"contrato_{pk}"]
    if contrato.cliente:
        filename_parts.append(contrato.cliente.razon_social.replace(" ", "_"))
    if contrato.auto:
        filename_parts.append(contrato.auto.patente)
    elif contrato.flota:
        filename_parts.append(contrato.flota.descripcion.replace(" ", "_"))

    response['Content-Disposition'] = f'attachment; filename="{"_".join(filename_parts)}.pdf"'
    
    # IMPORTANT: Reset the locale to default or a known state after your operation
    # This prevents side effects on other parts of your application.
    locale.setlocale(locale.LC_TIME, '') # Resets to default system locale or 'C'
    
    return response


###########################################################################################################
# INFRACCIONES
###########################################################################################################

# Vista para listar todas las infracciones
@login_required
def listado_infracciones(request):
    infracciones = Infracciones.objects.all()
    return render(request, 'infracciones/infraccion_list.html', {'infracciones': infracciones})

# Vista para agregar una nueva infracción
@login_required
def agregar_infraccion(request):
    if request.method == 'POST':
        form = InfraccionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_infracciones')  # Redirige al listado de infracciones
    else:
        form = InfraccionesForm()
    return render(request, 'infracciones/agregar_infraccion.html', {'form': form})

# Vista para editar una infracción existente
@login_required
def editar_infraccion(request, pk):
    infraccion = get_object_or_404(Infracciones, pk=pk)
    if request.method == 'POST':
        form = InfraccionesForm(request.POST, instance=infraccion)
        if form.is_valid():
            form.save()
            return redirect('listado_infracciones')  # Redirige al listado después de guardar
    else:
        form = InfraccionesForm(instance=infraccion)
    return render(request, 'infracciones/editar_infraccion.html', {'form': form})

# Vista para eliminar una infracción
@login_required
def eliminar_infraccion(request, pk):
    infraccion = get_object_or_404(Infracciones, pk=pk)
    infraccion.delete()
    return redirect('listado_infracciones')  # Redirige al listado de infracciones



####################################################################################################################################
# SINIESTROS
####################################################################################################################################
from django.db.models import F  # Para actualizaciones eficientes

@login_required
def listado_siniestro(request):
    siniestros = Siniestro.objects.all()
    return render(request, 'seguros/siniestros/siniestro_list.html', {'siniestros': siniestros})

@login_required
def agregar_siniestro(request):
    if request.method == 'POST':
        form = SiniestroForm(request.POST)
        if form.is_valid():
            form.save()
            automovil = form.cleaned_data['vehiculo']  # Extrae el valor del campo
            fecha_siniestro = form.cleaned_data['fecha']  # Extrae el valor del campo

            
            if automovil:
                # Incrementar el campo uso en 1 de forma eficiente
                fecha_siniestro = Siniestro.objects.filter
                Automovil.objects.filter(id=automovil.id).update(cantidad_de_sinistros=F('cantidad_de_sinistros') + 1)
                Automovil.objects.filter(id=automovil.id).update(fecha_ultimo_siniestro = fecha_siniestro)

        

            return redirect('listado_siniestro')  # Redirige al listado de siniestros
    else:
        form = SiniestroForm()
    return render(request, 'seguros/siniestros/agregar_siniestro.html', {'form': form})

@login_required
def eliminar_siniestro(request, pk):
    siniestro = get_object_or_404(Siniestro, pk=pk)
    automovil = siniestro.vehiculo  # Obtener el automóvil asociado al siniestro
    siniestro.delete()

    Automovil.objects.filter(id=automovil.id).update(cantidad_de_sinistros=F('cantidad_de_sinistros') - 1)
        

    return redirect('listado_siniestro')  # Redirige al listado de siniestros

@login_required
def editar_siniestro(request, pk):
    siniestro = get_object_or_404(Siniestro, pk=pk)
    if request.method == 'POST':
        form = SiniestroForm(request.POST, instance=siniestro)
        if form.is_valid():
            form.save()
            return redirect('listado_siniestro')  # Redirige al listado después de guardar
    else:
        form = SiniestroForm(instance=siniestro)
    return render(request, 'seguros/siniestros/editar_siniestro.html', {'form': form})


####################################################################################################################################

@login_required
def home(request):
    N = notas.objects.all()
    return render(request, 'index.html', {'notas': N})
    

@login_required
def barra_navegacion(request):
    opciones_menu = ['Automoviles', 'Clientes', 'VTV', 'Seguros','Patentes','Mantenimiento']
    return render(request, 'bnav.html', {'opciones_menu': opciones_menu})

@login_required
def eliminar_nota(request, pk):
    nota = get_object_or_404(notas, pk=pk)
    nota.delete()
    return redirect('home')


####################################################################################################################################



@login_required
def menu_automoviles(request):
    flota_id = request.GET.get('flota_id', None)  # Obtén el estado de la VTV desde los parámetros GET
    estado_vtv = request.GET.get('estado_vtv', None)  # Obtén el estado de la VTV desde los parámetros GET

    automoviles = Automovil.objects.filter(visibilidad=True)
#     # Obtener todos los estados posibles para mostrarlos como opciones en el filtro
    estados_vtv = VtvEstado.objects.all()
    flotas = Flota.objects.all()


    if estado_vtv:  # Aplica el filtro si se especifica un estado
        automoviles = automoviles.filter(vtv__estado__estado=estado_vtv)

    if flota_id:
        automoviles = automoviles.filter(flota__id=flota_id)


    return render(request, 'automovil/automoviles.html', {
        'autos': automoviles,
        'estados_vtv': estados_vtv,
        'flotas': flotas,
        'estado_seleccionado': estado_vtv,
        'flota_seleccionada': flota_id,
    })

@login_required
def menu_clientes(request):

    cliente = {'nombre': Cliente.nombre,
            'apellido':Cliente.apellido,
            'dni':Cliente.dni,
            'cuil':Cliente.cuil,
            'direccion':Cliente.direccion,
            'tel':Cliente.telefono,
            'email':Cliente.email}
    
    return render(request, 'clientes/clientes_list.html', cliente)

@login_required
def alta_automovil(request):
    if request.method == 'POST':
        form = AutomovilForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo objeto Automovil
            return redirect('listado_automoviles')  #
    else:
        form = AutomovilForm()
        form.fields.pop("flota")

    return render(request, 'automovil/alta_automovil.html', {'form': form})

@login_required
def eliminar_automovil(request, auto_id):
    auto = get_object_or_404(Automovil, id=auto_id)
    auto.visibilidad = False  # Cambia visibilidad a False
    auto.save()  # Guarda el cambio en la base de datos
    return redirect('listado_automoviles')  # Redirige a la lista después

@login_required
def editar_automovil(request, auto_id):
    auto = get_object_or_404(Automovil, id=auto_id)

    if request.method == 'POST':
        form = AutomovilForm(request.POST, instance=auto)
        if form.is_valid():
            form.save()
            return redirect('listado_automoviles')  # Redirige a la lista después de guardar
    else:
        form = AutomovilForm(instance=auto)

    return render(request, 'automovil/editar_automovil.html', {'form': form, 'auto': auto})

@login_required
def detalle_automovil(request, auto_id):
    auto = get_object_or_404(Automovil, id=auto_id)
    turnos = Turno_VTV.objects.filter(auto=auto_id).order_by('-fecha_turno')  # Obtener todos los turnos del auto
    # siniestros = Siniestro.objects.filter(auto=auto_id).order_by('-fecha_ultimo_siniestro')  
    
    # Obtener la fecha del filtro del formulario
    # fecha_filtro = request.GET.get('fecha_turno')
    
    # if fecha_filtro:  # Si se ha seleccionado una fecha
    #     fecha_filtro = parse_date(fecha_filtro)  # Convertir la fecha en formato válido
    #     if fecha_filtro:
    #         turnos = turnos.filter(fecha_turno__date=fecha_filtro)  # Filtrar por la fecha exacta

    return render(request, 'automovil/detalle_automovil.html', {'auto': auto , 'turnos':turnos })




#############################################################################################################################################
# LOGIN
#############################################################################################################################################



def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a la vista principal después del login
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})



##################################################################################################################################
# CLIENTES
##################################################################################################################################

@login_required
def listado_clientes(request):

    clientes = Cliente.objects.filter(visible=True)
    return render(request, 'clientes/clientes_list.html', {'clientes': clientes})


@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_clientes')  # Redirige al listado de clientes
    else:
        form = ClienteForm()
    return render(request, 'clientes/agregar_cliente.html', {'form': form})


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.visible = False  # Oculta el cliente
    cliente.save()
    return redirect('listado_clientes')  # Redirige al listado de clientes


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listado_clientes')  # Redirigir al listado después de guardar
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form})





#####################################################################################################################

# SERVICIOS
#####################################################################################################################


@login_required
def listado_servicios(request):

    servicios = Servicio.objects.all()
    return render(request, 'servicios/servicios_list.html', {'servicios': servicios})


@login_required
def agregar_servicios(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_servicios')  # Redirige al listado de clientes
    else:
        form = ServicioForm()
    return render(request, 'servicios/agregar_servicios.html', {'form': form})


@login_required
def eliminar_servicios(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    servicio.delete()
    return redirect('listado_servicios')  # Redirige al listado de clientes



@login_required
def editar_servicios(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('listado_servicios')  # Redirigir al listado después de guardar
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'servicios/editar_servicios.html', {'form': form})




#####################################################################################################################
# vtv
######################################################################################################################
@login_required
def listado_turno_vtv(request):
    # Lógica para registrar turnos
    turnos_vtv = Turno_VTV.objects.filter(estado='pendiente')
    return render(request, 'vtv/listado_turno_vtv.html', {'turnos_vtv': turnos_vtv})
    
@login_required
def alta_turno_vtv(request):
    if request.method == 'POST':
        form = TurnoVTVForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_turno_vtv')  # Redirige a una lista de turnos o la página que consideres apropiada
    else:
        form = TurnoVTVForm()
    return render(request, 'vtv/alta_turno.html', {'form': form})

@login_required
def eliminar_turno_vtv(request, pk):
    turno = get_object_or_404(Turno_VTV, pk=pk)
    
    if request.method == 'POST':
        turno.estado = 'cancelado'
        turno.save()
        return redirect('listado_turno_vtv')  # Redirige a la lista de turnos después de cancelar uno

@login_required
def editar_turno_vtv(request, pk):
    turno = get_object_or_404(Turno_VTV, pk=pk)

    if request.method == 'POST':
        form = TurnoVTVForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('listado_turno_vtv')  # Redirige a la lista de turnos después de editar uno
    else:
        form = TurnoVTVForm(instance=turno)
    
    return render(request, 'vtv/editar_turno.html', {'form': form, 'turno': turno})




###########################################################################################################################
# FLOTA
###########################################################################################################################

@login_required
def listado_flota(request):
    
    # Obtener todos los estados posibles para mostrarlos como opciones en el filtro
    flota = Flota.objects.all()

    return render(request, 'flota/listado_flota.html', {'flota': flota})

@login_required
def alta_flota(request):
    if request.method == 'POST':
        form = FlotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_flota')  # Redirige a una lista de turnos o la página que consideres apropiada
    else:
        form = FlotaForm()
    return render(request, 'flota/alta_flota.html', {'form': form})

@login_required
def eliminar_flota(request, pk):
    flota = get_object_or_404(Flota, pk=pk)
    if not Automovil.objects.filter(flota=flota).exists():
        flota.delete()
        messages.success(request, "La flota ha sido eliminada con éxito.")
    else:
        messages.error(request, "No se puede eliminar la flota porque tiene automóviles asociados.")

        
    return redirect('listado_flota')  # Redirige a la lista después de cancelar uno

@login_required
def asociar_automovil(request, pk):
    if request.method == 'POST':
        flota = get_object_or_404(Flota, pk=pk)
        automovil_id = request.POST.get('automovil_id')
        automovil = get_object_or_404(Automovil, id=automovil_id)
        automovil.flota = flota
        automovil.save()

        flota.disponible = True
        flota.save()


        return redirect('editar_flota', pk=pk)

@login_required
def editar_flota(request, pk):
    flota = get_object_or_404(Flota, pk=pk)
    automoviles_asociados = Automovil.objects.filter(flota=flota).filter(visibilidad=True)
    automoviles_restantes = Automovil.objects.exclude(flota=flota).filter(visibilidad=True)

    if request.method == 'POST':
        form = FlotaForm(request.POST, instance=flota)
        if form.is_valid():
            form.save()
            return redirect('listado_flota')  # Redirigir al listado después de guardar
    else:
        form = FlotaForm(instance=flota)
    return render(request, 'flota/editar_flota.html', {
        'form': form,
        'flota': flota,
        'automoviles_asociados': automoviles_asociados,
        'automoviles_restantes': automoviles_restantes,
})

@login_required
def eliminar_asociacion(request, pk, auto_id):
    flota = get_object_or_404(Flota, pk=pk)
    automovil = get_object_or_404(Automovil, id=auto_id)
    
    # Desasociar el automóvil de la flota
    if automovil.flota == flota:
        automovil.flota = None
        automovil.save()

    # Verificar si quedan automóviles asociados a la flota
    if not Automovil.objects.filter(flota=flota).exists():
        flota.disponible = True
        flota.save()

    return redirect('editar_flota', pk=pk)

@login_required
def detalle_flota(request, pk):
    flota = get_object_or_404(Flota, pk=pk) 
    automoviles_asociados = Automovil.objects.filter(flota=flota).filter(visibilidad=True)
    automoviles_restantes = Automovil.objects.exclude(flota=flota).filter(visibilidad=True)

    if request.method == 'POST':
        form = FlotaForm(request.POST, instance=flota)
        if form.is_valid():
            form.save()
            return redirect('detalle_flota')  # Redirigir al listado después de guardar
    else:
        form = FlotaForm(instance=flota)
    return render(request, 'flota/detalle_flota.html', {
        'form': form,
        'flota': flota,
        'automoviles_asociados': automoviles_asociados,
        'automoviles_restantes': automoviles_restantes,
})



####################################################################################################################
# TITULAR
####################################################################################################################

@login_required
def listado_titular(request):

    titulares = Titular.objects.all()
    return render(request, 'titular/titular_list.html', {'titulares': titulares})

@login_required
def agregar_titular(request):
    if request.method == 'POST':
        form = TitularForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('titular_listado')  # Redirige al listado de clientes
    else:
        form = TitularForm()
    return render(request, 'titular/agregar_titular.html', {'form': form})


@login_required
def eliminar_titular(request, pk):
    titular = get_object_or_404(Titular, pk=pk)
    titular.delete()
    return redirect('titular_listado')  # Redirige al listado de clientes


@login_required
def editar_titular(request, pk):
    titular = get_object_or_404(Titular, pk=pk)
    if request.method == 'POST':
        form = TitularForm(request.POST, instance=titular)
        if form.is_valid():
            form.save()
            return redirect('titular_listado')  # Redirigir al listado después de guardar
    else:
        form = TitularForm(instance=titular)
    return render(request, 'titular/editar_titular.html', {'form': form})



####################################################################################################################
# ASEGURADORAS
####################################################################################################################

@login_required
def listado_aseguradoras(request):

    aseguradora = Aseguradora.objects.all()
    return render(request, 'seguros/aseguradoras/Aseguradora_list.html', {'Aseguradoras': aseguradora})


@login_required
def agregar_aseguradoras(request):
    if request.method == 'POST':
        form = AseguradoraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aseguradoras_listado')  # Redirige al listado de clientes
    else:
        form = AseguradoraForm()
    return render(request, 'seguros/aseguradoras/agregar_Aseguradora.html', {'form': form})


@login_required
def eliminar_aseguradoras(request, pk):
    aseguradora = get_object_or_404(Aseguradora, pk=pk)
    aseguradora.delete()
    return redirect('aseguradoras_listado')  # Redirige al listado de clientes


@login_required
def editar_aseguradoras(request, pk):
    aseguradora = get_object_or_404(Aseguradora, pk=pk)
    if request.method == 'POST':
        form = AseguradoraForm(request.POST, instance=aseguradora)
        if form.is_valid():
            form.save()
            return redirect('aseguradoras_listado')  # Redirigir al listado después de guardar
    else:
        form = AseguradoraForm(instance=aseguradora)
    return render(request, 'seguros/aseguradoras/editar_aseguradora.html', {'form': form})

###################################################################################################################
# POLIZA
###################################################################################################################

@login_required
def listado_poliza(request):
    
    poliza = PolizaSeguro.objects.all()
    return render(request, 'seguros/polizas/Poliza_list.html', {'polizas': poliza})

@login_required
def agregar_poliza(request):
    if request.method == 'POST':
        form = PolizaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listado_poliza')  # Redirige a una lista de turnos o la página que consideres apropiada
    else:
        form = PolizaForm()
    return render(request, 'seguros/polizas/agregar_Poliza.html', {'form': form})


@login_required
def eliminar_poliza(request, pk):
    poliza = get_object_or_404(PolizaSeguro, pk=pk)
    poliza.delete()
    return redirect('listado_poliza')  # Redirige al listado de clientes

@login_required
def editar_poliza(request, pk):
    poliza = get_object_or_404(PolizaSeguro, pk=pk)
    if request.method == 'POST':
        form = PolizaForm(request.POST, instance=poliza)
        if form.is_valid():
            form.save()
            return redirect('listado_poliza')  # Redirigir al listado después de guardar
    else:
        form = PolizaForm(instance=poliza)
    return render(request, 'seguros/polizas/editar_Poliza.html', {'form': form})




###################################################################################################################
#  MANTENIEMIENTO
###################################################################################################################

def listado_mantenimiento(request):
    mantenimientos = HistorialMantenimiento.objects.all()
    return render(request, 'mantenimiento/listado_mantenimiento.html', {'mantenimientos': mantenimientos})

def agregar_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            vehiculo = form.cleaned_data['vehiculo']  # Extrae el valor del campo

            km_servicio = form.cleaned_data['km_servicio']  # Extrae el valor del campo
            fecha_servicio = form.cleaned_data['fecha_servicio_inicio']  # Extrae el valor del campo


            if vehiculo:
                # Incrementar el campo uso en 1 de forma eficiente
                auto = Automovil.objects.get(id=vehiculo.id)
                km_servicio_registrados= auto.kilometraje
                print(km_servicio_registrados)

                if km_servicio < km_servicio_registrados:
                    messages.error(request, "El kilometraje ingresado es menor al registrado.")
                    return render(request, 'mantenimiento/agregar_mantenimiento.html', {'form': form})
                else:
                
                    Automovil.objects.filter(id=vehiculo.id).update(kilometraje = km_servicio)
                    Automovil.objects.filter(id=vehiculo.id).update(km_ultimo_servicio = km_servicio)                
                    Automovil.objects.filter(id=vehiculo.id).update(fecha_ultimo_servicio = fecha_servicio)

                    form.save()
                    return redirect('listado_mantenimiento')  # Redirige al listado de clientes
    else:
        form = MantenimientoForm()
    return render(request, 'mantenimiento/agregar_mantenimiento.html', {'form': form})

def eliminar_mantenimiento(request, pk):
    mantenimiento = get_object_or_404(HistorialMantenimiento, pk=pk)
    mantenimiento.delete()
    return redirect('listado_mantenimiento')  # Redirige al listado de clientes

def editar_mantenimiento(request, pk):
    mantenimiento = get_object_or_404(HistorialMantenimiento, pk=pk)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            return redirect('listado_mantenimiento')  # Redirigir al listado después de guardar
    else:
        form = MantenimientoForm(instance=mantenimiento)
    return render(request, 'mantenimiento/editar_mantenimiento.html', {'form': form})


###################################################################################################################
#  LOGIN
###################################################################################################################


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('home')  # Redirige a la página principal
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})




###################################################################################################################



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import notas
import json

@csrf_exempt
def crear_nota(request):
    if request.method == "POST":
        data = request.POST
        nueva_nota = notas.objects.create(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            fecha=data["fecha"],
            prioridad=data["prioridad"]
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)



def advertencia_view(request):
    return render(request, '404.html')  # Vista de advertencia