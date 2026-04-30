from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CalificacionForm, RegistroUsuarioForm
from .models import Calificacion
from django.contrib import messages


def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('listar_calificaciones')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registration/registro.html', {
        'form': form
    })


@login_required
def listar_calificaciones(request):
    calificaciones = Calificacion.objects.all()
    promedio_general = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg']

    return render(request, 'calificaciones/listar.html', {
        'calificaciones': calificaciones,
        'promedio_general': promedio_general
    })


@login_required
def crear_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'La calificación fue registrada correctamente.') 
            return redirect('listar_calificaciones')
    else:
        form = CalificacionForm()

    return render(request, 'calificaciones/crear.html', {
        'form': form
    })


@login_required
def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)

    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)

        if form.is_valid():
            form.save()
            messages.success(request, 'La calificación fue actualizada correctamente.')
            return redirect('listar_calificaciones')
    else:
        form = CalificacionForm(instance=calificacion)

    return render(request, 'calificaciones/editar.html', {
        'form': form,
        'calificacion': calificacion
    })


@login_required
def eliminar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)

    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, 'La calificación fue eliminada correctamente.')
        return redirect('listar_calificaciones')

    return render(request, 'calificaciones/eliminar.html', {
        'calificacion': calificacion
    })


@login_required
def promedio_general(request):
    promedio = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg']

    return render(request, 'calificaciones/promedio_general.html', {
        'promedio_general': promedio
    })