from django.shortcuts import render
from urllib2 import urlopen
import urllib2
from bs4 import BeautifulSoup
from .models import Equipo;


def obtener_titulo(request):

	serie  = '62672'
	fecha  = '30/12/2016'
	modelo = 'PC300LC-8'
 	url = 'http://komtrax.kcl.cl/mailing/diario/operacion/operacion.php?Serie='+ serie +'&Fecha='+ fecha +'&Modelo='+ modelo
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page,'html.parser')
	finds = (soup.find_all('span')[6:8])
	list = []
	for find in finds:
		list.append(find.text.encode("utf-8"))
		print find.string
	
	params = {

		'list' : list
		
	}
	return render(request,'cial/index.html', params)

def obtener_equipo(request):
	consulta = request.GET.get('q', '') 
	equipo = Equipo.objects.filter().order_by('id')
	return render(request,'cial/Index2.html',{'equipo':equipo})