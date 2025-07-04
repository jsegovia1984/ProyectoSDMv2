from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Automovil, ClienteParticular

class AutomovilForm(forms.ModelForm):
    class Meta:
        model = Automovil
        fields = '__all__'  # Incluye todos los campos del modelo
        exclude = ['visibilidad']  # Sustituye con el nombre del campo que deseas ocultar

        widgets = {
            'anio': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'kilometraje': forms.NumberInput(attrs={'min': 0}),
            'patente': forms.TextInput(attrs={'placeholder': 'ABC123'}),
            

        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))



class ClienteForm(forms.ModelForm):
    class Meta:
        model = ClienteParticular
        fields = '__all__'  # Incluye todos los campos del modelo
        exclude = ['visible']  # Sustituye con el nombre del campo que deseas ocultar

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'cuil': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }



class ClienteForm(forms.ModelForm):
    class Meta:
        model = ClienteParticular
        fields = ['nombre', 'apellido', 'dni', 'cuil', 'direccion', 'telefono', 'email']  # Excluir explícitamente otros campos
