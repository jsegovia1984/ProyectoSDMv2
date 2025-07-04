from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Automovil, Cliente , Servicio
from .models import Turno_VTV
from .models import Flota,Titular,Aseguradora,PolizaSeguro,HistorialMantenimiento,Siniestro,Infracciones,Contrato


class InfraccionesForm(forms.ModelForm):
    class Meta:
        model = Infracciones
        fields = '__all__'  # Incluye todos los campos del modelo
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'monto': forms.NumberInput(attrs={'min': 0}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['auto'].queryset = Automovil.objects.filter(visibilidad=True)

class SiniestroForm(forms.ModelForm):
    class Meta:
        model = Siniestro
        fields = '__all__'  # Incluye todos los campos del modelo
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['vehiculo'].queryset = Automovil.objects.filter(visibilidad=True)

class AutomovilForm(forms.ModelForm):
    class Meta:
        model = Automovil
        fields = '__all__'  # Incluye todos los campos del modelo
        exclude=['visibilidad', 'fecha_ultimo_servicio', 'fecha_ultimo_siniestro', 'km_ultimo_servicio']
        widgets = {

            'anio': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'kilometraje': forms.NumberInput(attrs={'min': 0}),
            'patente': forms.TextInput(attrs={'placeholder': 'ABC123'}),

        }
    anio = forms.CharField(label='Año')

class FlotaForm(forms.ModelForm):
    class Meta:
        model = Flota
        fields = '__all__'  # Incluye todos los campos del modelo
        exclude=['visibilidad']
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Cantidad de unidades y descripción'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['cliente'].queryset = Cliente.objects.filter(visible=True)
    
class TitularForm(forms.ModelForm):
    class Meta:
        model = Titular
        fields = '__all__'  # Incluye todos los campos del modelo
 
    


    
class AseguradoraForm(forms.ModelForm):
    class Meta:
        model = Aseguradora
        fields = '__all__'  # Incluye todos los campos del modelo
 


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'  # Incluye todos los campos del modelo
        exclude = ['visible']  # Sustituye con el nombre del campo que deseas ocultar

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cuit': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }



class TurnoVTVForm(forms.ModelForm):
    class Meta:
        model = Turno_VTV
        fields = ['auto', 'fecha_turno', 'lugar_verificacion', 'comentarios']
        widgets = {
            'fecha_turno': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['auto'].queryset = Automovil.objects.filter(visibilidad=True)


class PolizaForm(forms.ModelForm):
    class Meta:
        model = PolizaSeguro
        fields = '__all__'  # Incluye todos los campos del modelo

        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'fecha_fin': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),

        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'  # Incluye todos los campos del modelo


class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = HistorialMantenimiento
        fields = '__all__'  # Incluye todos los campos del modelo
        widgets = {
            'fecha_servicio_inicio': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),


            'fecha_servicio_fin': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['vehiculo'].queryset = Automovil.objects.filter(visibilidad=True)

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'  # Incluye todos los campos del modelo
      
        widgets = {
            'fecha_contrato_firmado': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['auto'].queryset = Automovil.objects.filter(visibilidad=True)
        self.fields['cliente'].queryset = Cliente.objects.filter(visible=True)
        self.fields['flota'].queryset = Flota.objects.filter(disponible=True)