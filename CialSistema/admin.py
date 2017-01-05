from django.contrib import admin

# Register your models here.
from .models import Modelo, Chofer , Equipo

admin.site.register(Chofer)
admin.site.register(Equipo)
admin.site.register(Modelo)