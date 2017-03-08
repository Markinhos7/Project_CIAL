from django.contrib import admin

# Register your models here.
from .models import Modelo, Chofer , Equipo, Obra, Operacion, Maquina , Operacion_maq_mes, Operacion_maq_dia

admin.site.register(Chofer)
admin.site.register(Equipo)
admin.site.register(Modelo)
admin.site.register(Obra)
admin.site.register(Operacion)
admin.site.register(Maquina)
admin.site.register(Operacion_maq_mes)
admin.site.register(Operacion_maq_dia)