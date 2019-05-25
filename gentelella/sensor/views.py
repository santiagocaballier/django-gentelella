from django.http import HttpResponse,JsonResponse
from django.template import Context, loader 
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from sensor.models import *

import json
from datetime import datetime
from random import randint

# Create your views here.
def set_data(request,_mac_address,_dataint,_datadec):
    result = 'FAIL\n'
    
    qsensor = Sensor.objects.filter(mac_address=_mac_address)
    if qsensor:
        sensor = qsensor[0] 
    
        dsen = DataSensor()
        dsen.data = float(str(_dataint) + '.' + str(_datadec))
        dsen.datetime = datetime.now()
        dsen.sensor = sensor    
        
        dsen.save()
        print(dsen)
        result = 'OK\n'
        
    return HttpResponse(result)

def test(request,_username):
    goal = []
    goal.append(randint(5,30))
    
    return HttpResponse(goal)

def refresh_graph(request,_sensor_name):
    graph_data = {} 
    sensor = Sensor.objects.get(nombre=_sensor_name)
    
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']  
    
    #Data
    dq = DataSensor.objects.filter(sensor = sensor, datetime__range=(start_date, end_date))
    obj = []
    if dq:
        for d in dq:
            data = {"datetime" : str(d.datetime.date()) + ' ' + str(d.datetime.time()),"value" : str(d.data)}
            obj.append(data)
    else:
        data = {}
    
    graph_data.update({"data" : obj})
    
    #Alarma
    try:
        alarma = Alarma.objects.get(sensor = sensor)
        graph_data.update({"goals" : alarma.valor})
    except ObjectDoesNotExist:
        graph_data.update({"goals" : ''})
    
    
    #Json    
    graph_data = json.dumps(graph_data)


    
    return JsonResponse(graph_data,safe=False)