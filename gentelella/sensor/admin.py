from django.contrib import admin
from .models import Sensor,DataSensor,Empresa,Alarma,Ubicacion,Tipo

# Register your models here.
admin.site.register(Sensor)
#admin.site.register(DataSensor)
admin.site.register(Empresa)
admin.site.register(Alarma)
admin.site.register(Ubicacion)

