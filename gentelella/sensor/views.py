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
        _sensor = qsensor[0] 
        
        qalarma = Alarma.objects.get(sensor=_sensor)
    
        dsen = DataSensor()
        dsen.data = float(str(_dataint) + '.' + str(_datadec))
        dsen.datetime = datetime.now()
        dsen.sensor = _sensor
        if qalarma:
            dsen.alarma_value_max = qalarma.valor_max
            dsen.alarma_value_min = qalarma.valor_min
        
        dsen.save()
        print(dsen)
        result = 'OK\n'
        
    return HttpResponse(result)


def refresh_graph(request,_sensor_name):
    graph_data = {} 
    sensor = Sensor.objects.get(nombre=_sensor_name)
    
    
    if request.GET['start_date']:
        start_date = request.GET['start_date']
    else:
        start_date = datetime.now().strftime("%Y-%m-%d 00:00")
    
    if request.GET['end_date']: 
        end_date = request.GET['end_date']
    else:
        end_date = datetime.now().strftime("%Y-%m-%d 23:59")
    
    
    #Data
    dq = DataSensor.objects.filter(sensor = sensor, datetime__range=(start_date, end_date))
    obj = []
    if dq:
        for d in dq:
            data = {"datetime" : str(d.datetime.date()) + ' ' + str(d.datetime.time()) , "value" : str(d.data) , "alarma_max": str(d.alarma_value_max),"alarma_min": str(d.alarma_value_min)}
            obj.append(data)
    else:
        data = {}
    
    graph_data.update({"data" : obj})
    
    #Alarma
    try:
        alarma = Alarma.objects.get(sensor = sensor)
        graph_data.update({"goal_max" : alarma.valor_max,"goal_min" : alarma.valor_min})
    except ObjectDoesNotExist:
        graph_data.update({"goal_max" : '',"goal_min" : ''})
    
    
    #Json    
    graph_data = json.dumps(graph_data)


    
    return JsonResponse(graph_data,safe=False)

def refresh_ubicacion(request,_ubicacion_name):
    confort_acum = 0.00
    confort_count = 0
    
    if request.GET['start_date']:
        start_date = request.GET['start_date']
    else:
        start_date = datetime.now().strftime("%Y-%m-%d 00:00")
    if request.GET['end_date']: 
        end_date = request.GET['end_date']
    else:
        end_date = datetime.now().strftime("%Y-%m-%d 23:59")
    
    
    #Devolver una  tabla en Json con cada sensor y validacion de alarma.
    '''
    #    Calidad de aire    Temperatura    Luminosidad    Intensidad sonora    Factor de cumplimiento
    1    Dato 1    Dato 2    Dato 3    Dato 4    0%

              Sonido
              Aire
              Luminosidad
              Temperatura
              
              <tr>
                <th scope="row">1</th>
                <td id = "td_aire">Dato 1</td>
                <td id = "td_temp">Dato 2</td>
                <td id = "td_lumi">Dato 3</td>
                <td id = "td_sono">Dato 4</td>
                <td id = "td_cumplimiento">0%</td>
              </tr>
    '''

    jssensores = {}
    obj_datos = []

    #Obtengo los sensores
    dqsensor = Sensor.objects.filter(ubicacion__nombre = _ubicacion_name)
        
    if dqsensor:
        #Cada sensor
        for s in dqsensor:
            count_total = 0.00
            count_invalid = 0.00
            
            dq = DataSensor.objects.filter(sensor = s, datetime__range=(start_date, end_date))
            #Cada data en sensor
            if dq:
                for d in dq:
                    count_total += 1
                    if d.data <= d.alarma_value_min:
                        count_invalid +=1
                    elif d.data >= d.alarma_value_max:
                        count_invalid +=1
   
            cumplimiento = 0
            cumplimiento_texto = 'SIN DATOS'
            
            if count_total > 0:
                cumplimiento = (1 -(count_invalid / count_total)) * 100
                if count_invalid > 0:
                    cumplimiento_texto = 'NO CUMPLE'
                else:
                    cumplimiento_texto = 'CUMPLE'
            
            
            data_sonido = {}
            data_aire = {}
            data_luminosidad = {}
            data_temperatura = {}
            data_confort = {}
            
            if s.tipo.tipo == "Sonido":
                data_sonido = {"tipo" : "Sonido" , "cumplimiento" : cumplimiento,"cumplimiento_texto":cumplimiento_texto}
                print(count_total)
                print(data_sonido)
                obj_datos.append(data_sonido)
                #Armo el cumplimiento
                if cumplimiento_texto != 'SIN DATOS':
                    confort_acum = confort_acum + cumplimiento
                    confort_count = confort_count + 1
                
            if s.tipo.tipo == "Aire":
                data_aire  = {"tipo" : "Aire" , "cumplimiento" : cumplimiento,"cumplimiento_texto":cumplimiento_texto}
                print(cumplimiento_texto)
                print(data_aire)
                obj_datos.append(data_aire)
                #Armo el cumplimiento
                if cumplimiento_texto != 'SIN DATOS':
                    confort_acum = confort_acum + cumplimiento
                    confort_count = confort_count + 1
            
            if s.tipo.tipo  == "Luminosidad":
                data_luminosidad = {"tipo" : "Luminosidad" , "cumplimiento" : cumplimiento,"cumplimiento_texto":cumplimiento_texto}
                print(count_total)
                print(data_luminosidad)
                obj_datos.append(data_luminosidad)
                #Armo el cumplimiento
                if cumplimiento_texto != 'SIN DATOS':
                    confort_acum = confort_acum + cumplimiento
                    confort_count = confort_count + 1
                
            if s.tipo.tipo  == "Temperatura":
                data_temperatura = {"tipo" : "Temperatura" , "cumplimiento" : cumplimiento,"cumplimiento_texto":cumplimiento_texto}
                print(count_total)
                print(data_temperatura)
                obj_datos.append(data_temperatura)
                #Armo el cumplimiento
                if cumplimiento_texto != 'SIN DATOS':
                    confort_acum = confort_acum + cumplimiento
                    confort_count = confort_count + 1
            
            
            #datas = {"sensor" : s.nombre, "tipo" : s.tipo.tipo ,"data":obj_data,"cumplimiento" : cumplimiento ,"cumplimiento_texto" : cumplimiento_texto, "total_muestras" : count_total}
            #obj_sensores.append(datas)
    if confort_count > 0:
        confort_index = (1/confort_count) * confort_acum
        data_confort = {"confort_index" : confort_index}
        #obj_datos.append(data_confort)
    else:
        data_confort = {"confort_index" : 'SIN DATOS'}
        #obj_datos.append(data_confort)                     
    
    jssensores.update({"table_ubicacion" : obj_datos})
    jssensores.update({"data_confort" : data_confort})
    
    
    #Json    
    table_data = json.dumps(jssensores)
    
    
    return JsonResponse(table_data,safe=False)

