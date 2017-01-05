
from __future__ import unicode_literals

from django.db import models

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

    def __unicode__(self):
              return self.nombre_equipo

    