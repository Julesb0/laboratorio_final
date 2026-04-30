from django import forms
from django.contrib.auth.models import User
from .models import Calificacion


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        exclude = ['promedio']


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