import json
from django.core import serializers
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from sensor.models import *

#Esta vsta ataja la url '/' (vacia)
def index(request):
    context = {'username':request.user.username}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def gentelella_html(request):
    context = {'username':request.user.username}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

#******************************************************************************


def login_user(request):
    #Esta linea deslogue siempre que se llame a login.html
    logout(request)
    
    username = password = login_result = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            login_result = 'Verifique los datos ingresados'

    context = {'username':request.user.username, 'login_result':login_result, }
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

def dash_sensor(request):
    #Genero dinamicamente el combo sensores
    cs = Sensor.objects.filter(empresa__usuario__username = request.user.username)
    combo_sensor = cs
    
    #Genero dinamicamente el combo empresa
    ce = Empresa.objects.filter(usuario__username = request.user.username)
    combo_empresa = ce

    context = {'username':request.user.get_full_name(),'combo_sensor' : combo_sensor,'combo_empresa' : combo_empresa}
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

def dash_ubicacion(request):
    #Genero dinamicamente el combo ubicacion
    cu = Ubicacion.objects.filter(empresa__usuario__username = request.user.username)
    combo_ubicacion = cu
        
    #Genero dinamicamente el combo empresa
    ce = Empresa.objects.filter(usuario__username = request.user.username)
    combo_empresa = ce

    context = {'username':request.user.get_full_name(),'combo_ubicacion' : combo_ubicacion,'combo_empresa' : combo_empresa}
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))








