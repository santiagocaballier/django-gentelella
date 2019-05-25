from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ManyToManyField(User)

    def __str__(self):
        return self.nombre
    
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=254)
    empresa = models.ForeignKey(Empresa,on_delete=None,default=0)
    
    def __str__(self):
        return self.nombre
    
class Sensor(models.Model):
    nombre = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=12) #a020a60726d1
    empresa = models.ForeignKey(Empresa,on_delete=None,default=0)
    ubicacion = models.ForeignKey(Ubicacion,on_delete=None,default=0)
    
    def __str__(self):
        return self.nombre

class Alarma(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    valor = models.FloatField(default=0)
    descripcion = models.CharField(max_length=100,default="")
    
    def __str__(self):
        return self.sensor.nombre
    
class DataSensor(models.Model):
    sensor =  models.ForeignKey(Sensor,on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    data = models.FloatField()
    
    def __str__(self):
        return str(self.datetime) + ' - ' + str(self.data)
    
