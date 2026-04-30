from django import forms
from django.contrib.auth.models import User
from .models import Calificacion


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        exclude = ['promedio']

        labels = {
            'nombre_estudiante': 'Nombre del estudiante',
            'identificacion': 'Identificación',
            'asignatura': 'Asignatura',
            'nota1': 'Nota 1',
            'nota2': 'Nota 2',
            'nota3': 'Nota 3',
        }

        widgets = {
            'nombre_estudiante': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: Ana Martínez'
            }),
            'identificacion': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: 1234567890'
            }),
            'asignatura': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: Matemáticas'
            }),
            'nota1': forms.NumberInput(attrs={
                'min': '0',
                'max': '5',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'nota2': forms.NumberInput(attrs={
                'min': '0',
                'max': '5',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'nota3': forms.NumberInput(attrs={
                'min': '0',
                'max': '5',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }

    def validar_nota(self, nota):
        if nota is None:
            return nota

        if nota < 0 or nota > 5:
            raise forms.ValidationError('La nota debe estar entre 0.0 y 5.0.')

        return nota

    def clean_nota1(self):
        return self.validar_nota(self.cleaned_data.get('nota1'))

    def clean_nota2(self):
        return self.validar_nota(self.cleaned_data.get('nota2'))

    def clean_nota3(self):
        return self.validar_nota(self.cleaned_data.get('nota3'))


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password_confirmacion = forms.CharField(widget=forms.PasswordInput, label='Confirmar contraseña')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmacion = cleaned_data.get('password_confirmacion')

        if password and password_confirmacion and password != password_confirmacion:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user