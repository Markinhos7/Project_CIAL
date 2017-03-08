
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal

class Modelo(models.Model):
    nombre_modelo       = models.CharField(max_length=50)
    descripcion_modelo  = models.CharField(max_length=100)
    def __unicode__(self):
              return self.nombre_modelo
class Chofer(models.Model):
    nombre_chofer       = models.CharField(max_length=50)
    descripcion_chofer  = models.CharField(max_length=100)
    rut_chofer          = models.CharField(max_length=10)
    fono_chofer         = models.IntegerField()

    def __unicode__(self):
              return self.nombre_chofer 

class Equipo(models.Model):
    nombre_equipo      = models.CharField(max_length=50)
    descripcion_equipo = models.CharField(max_length=100)
    patente_equipo     = models.CharField(max_length=10)
    serie_equipo       = models.CharField(max_length=100)
    Modelo_equipo      = models.ForeignKey('Modelo', on_delete=models.CASCADE)
    chofer             = models.ForeignKey('Chofer', on_delete=models.CASCADE)
    obra               = models.ForeignKey('Obra', on_delete=models.CASCADE)
    horometro          = models.IntegerField()
    rendimiento        = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    
    def __unicode__(self):
              return self.nombre_equipo + '-'+self.patente_equipo
class Maquina(models.Model):
    movil    =  models.CharField(max_length=50)
    patente  =  models.CharField(max_length=50)
    fecha    =  models.CharField(max_length=50)
    hora     =  models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    longitud =  models.IntegerField()
    latitud  =  models.IntegerField()
    evento   =  models.CharField(max_length=50)

    def __unicode__(self):
              return self.hora + self.patente
              
class Operacion_maq_mes(models.Model):
    hora = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    Modelo = models.CharField(max_length=50)
    patente = models.CharField(max_length=50)
    mes = models.CharField(max_length=50)

    def __unicode__(self):
              return self.hora + self.patente

class Operacion_maq_dia(models.Model):
    hora = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    Modelo =models.CharField(max_length=50)
    patente = models.CharField(max_length=50)
    mes = models.CharField(max_length=50)
    
    def __unicode__(self):
              return self.hora + self.patente

class Obra(models.Model):
    nombre_obra      = models.CharField(max_length=50)
    descripcion_obra = models.CharField(max_length=100)

    def __unicode__(self):
              return self.nombre_obra

class Operacion(models.Model):
    DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
    hora_diaria = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    operacion_real = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    relentis = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    consumo_combustible = models.CharField(max_length=50)
    rendimiento_promedio = models.DecimalField(max_digits=20,decimal_places=1,default=Decimal('0.0')) 
    fecha = models.DateField()
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE )

    def __unicode__(self):
              return self.equipo.serie_equipo + " - " +self.fecha.strftime('%d/%m/%Y') 




                