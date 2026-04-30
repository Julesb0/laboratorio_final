from django import forms
from django.contrib.auth.models import User
from .models import Calificacion


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        exclude = ['promedio']

    def clean_nota1(self):
        nota = self.cleaned_data.get('nota1')

        if nota < 0 or nota > 5:
            raise forms.ValidationError('La nota debe estar entre 0.0 y 5.0.')

        return nota

    def clean_nota2(self):
        nota = self.cleaned_data.get('nota2')

        if nota < 0 or nota > 5:
            raise forms.ValidationError('La nota debe estar entre 0.0 y 5.0.')

        return nota

    def clean_nota3(self):
        nota = self.cleaned_data.get('nota3')

        if nota < 0 or nota > 5:
            raise forms.ValidationError('La nota debe estar entre 0.0 y 5.0.')

        return nota


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