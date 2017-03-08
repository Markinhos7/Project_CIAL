# -*- coding: utf-8 -*-
from django.shortcuts import render
from urllib2 import urlopen
import urllib2
from bs4 import BeautifulSoup
from .models import Equipo , Modelo , Operacion , Maquina , Operacion_maq_dia, Obra
from .forms import ReporteForm , EntelForm
from io import BytesIO
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter ,landscape
from reportlab.platypus import Table
from reportlab.pdfgen import canvas
from cStringIO import StringIO
import re
import calendar
from django.shortcuts import render
from django.shortcuts import redirect
import datetime
from datetime import datetime , timedelta ,date
from decimal import Decimal
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.cell import *

def post_list(request):

	if request.method == 'POST':
		form = EntelForm(request.POST)
		
		if form.is_valid():
			fecha = request.POST['fecha']
			
			if obra == 'Paillaco':

				hora_entel()
				return redirect('/index2')

		else:
			
			form = EntelForm()	
	else:
			
		form = EntelForm() 
		
	return render(request, 'cial/Index2.html', {})


def GeneratePdf(request):

	if request.method == 'POST':
		form = ReporteForm(request.POST)
		
		if form.is_valid():
			obra = request.POST['obra']
			
			if obra == 'Paillaco':

				InsertOperacionRetroExcavadora('1')
				InsertOperacionExcavadora('1')
				return redirect('/index/1')
			if obra == 'Los angeles':

				InsertOperacionRetroExcavadora('2')
				InsertOperacionExcavadora('2')
				return redirect('/index/2')
			if obra == 'Tranapuente':

				
				InsertOperacionExcavadora('3')
				return redirect('/index/3')
			if obra == 'Pto saavedra':

				InsertOperacionRetroExcavadora('4')
				return redirect('/index/4')
			if obra == 'Renaico':

				InsertOperacionRetroExcavadora('5')
				return redirect('/index/5')
			if obra == 'Empalme Hinca Tco':

				InsertOperacionRetroExcavadora('6')
				return redirect('/index/6')	
		else:
			
			form = ReporteForm()	
	else:
			
		form = ReporteForm() 
		create_powerpoint()
		obtener_coordenadas()

	return render(request,'cial/index.html', {'form': form })

def obtener_titulo(serie,modelo):
	fecha  = '11/02/2017'
 	url = 'http://komtrax.kcl.cl/mailing/diario/operacion/operacion.php?Serie='+ serie +'&Fecha='+ fecha +'&Modelo='+ modelo
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page,'html.parser')
	finds = (soup.find_all('span')[6:8])
	list = []
	for find in finds:
		list.append(find.text.encode("utf-8"))
		print find.string

	return list

def obtener_titulo2(serie,modelo):
	fecha  = '06/02/2017'
 	url = 'http://komtrax.kcl.cl/frm_consultas/operacion/operacion_daily2.php?mes=03&anyo=2017&Serie='+ serie +'&Modelo='+ modelo	
 	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page,'html.parser')
	div  = soup.find("div" ,{ "id":"Layer1"}) 
	table = div.find("table", { "class" : "CobaltFormTABLE" })
	list = []
	rows = (table.findAll('tr')[0:1])
	for row in rows:
		cells = (row.findAll("td")[0:6])
		for cell in cells:
			list.append(cell.text.encode("utf-8"))
			
		list.append(serie.encode("utf-8"))
	return list
def InsertOperacionRetroExcavadora(obra):
	datos_serie1 	  = []
	modelo2      	  = 'PC300LC|8'
	equipo_retro      = Equipo.objects.filter(Modelo_equipo = '4', obra = obra ).select_related()
	fecha_actual 	  = date.today() - timedelta(days=1)
	for series in equipo_retro:
		datos_serie1.append(obtener_titulo(series.serie_equipo,series.Modelo_equipo.nombre_modelo))

	for series1 , series in zip(datos_serie1, equipo_retro ):
		
		try: 
			obj = Operacion.objects.get(equipo = series , fecha = datetime.strptime(series1[0], '%d/%m/%Y').strftime('%Y-%m-%d'))
			print "asdad"
		except Operacion.DoesNotExist:
			Operacion.objects.create(hora_diaria = Decimal(series1[1][0:3]), operacion_real = 0, relentis = 0, 
					consumo_combustible = 0 , rendimiento_promedio = 0,fecha = datetime.strptime(series1[0], '%d/%m/%Y').strftime('%Y-%m-%d'), equipo = series)

	return datos_serie1	


def InsertOperacionExcavadora(obra):
	
	datos_serie1 	     = []
	modelo2      	     = 'PC300LC|8'
	equipo_excavadora    = Equipo.objects.exclude(Modelo_equipo = '4').filter(obra = obra).select_related()
	fecha_actual = date.today() - timedelta(days=1)

	for series in equipo_excavadora:
		datos_serie1.append(obtener_titulo2(series.serie_equipo,series.Modelo_equipo.nombre_modelo))
		
	for datos , series  in zip(datos_serie1 , equipo_excavadora):
		
		try: 
			obj = Operacion.objects.get(equipo = series , fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d'))
			
			Operacion.objects.filter(equipo = series , fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d')).update(hora_diaria = datos[1].replace('Hrs.','') , operacion_real = datos[2].replace('Hrs.',''), relentis = float(float(datos[1].replace('Hrs.','')) - float(datos[2].replace('Hrs.',''))), 
				consumo_combustible = datos[4].replace('Lts.',''), rendimiento_promedio = Decimal(datos[3].replace('lt/hr','')),fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d'), equipo = series)
			print "asdad"
		except Operacion.DoesNotExist:

			if  Decimal(datos[3].replace('lt/hr','')) == 0.00:
				if datos[1].replace(' Hrs.','') == ''  and datos[4].replace('Lts.','') == '':

					Operacion.objects.create(hora_diaria = 0 , operacion_real = datos[2].replace('Hrs.',''), relentis = 0,
					consumo_combustible = 0, rendimiento_promedio = 0,fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d'), equipo = series)
				else:

					Operacion.objects.create(hora_diaria = datos[1].replace('Hrs.','') , operacion_real = datos[2].replace('Hrs.',''), relentis = float(float(datos[1].replace('Hrs.','')) - float(datos[2].replace('Hrs.',''))), 
					consumo_combustible = datos[4].replace('Lts.',''), rendimiento_promedio = Decimal(datos[3].replace('lt/hr','')),fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d'), equipo = series)
			else:	
				if (datos[1] == 'Hrs.'  ):

					Operacion.objects.create(hora_diaria = 0, operacion_real = datos[2].replace('Hrs.',''), relentis = 0, 
					consumo_combustible = 0, rendimiento_promedio = 0,fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d'), equipo = series)
				else:

					Operacion.objects.create(hora_diaria = datos[1].replace('Hrs.',''), operacion_real = datos[2].replace('Hrs.',''), relentis = Decimal(float(datos[1].replace('Hrs.','')) - float(datos[2].replace('Hrs.',''))), 
					consumo_combustible = datos[4].replace('Lts.',''), rendimiento_promedio = Decimal(Decimal(datos[4].replace('Lts.','')) / Decimal(datos[1].replace('Hrs.',''))),fecha = datetime.strptime(datos[0], '%d/%m/%Y').strftime('%Y-%m-%d'), equipo = series)

	return datos_serie1	

def obtener_coordenadas():
	from pyparsing import Literal, quotedString, removeQuotes, delimitedList
	url = 'http://komtrax.kcl.cl/mailing/diario/areafaena/areafaena.php?Serie=71778&Fecha=06/03/2017&Modelo=WA320-6'
	page=urllib2.urlopen(url)
	soup = BeautifulSoup(page , 'html.parser')
	sources=(soup.findAll("script")[1:2])
	
	hola = ""
	list = []
	for source in sources:
		buscar = source.find(text ="map.LoadMap(new VELatLong()")
		hola = source
		list.append(source)

	
	print list[0:1]		
	return list

def cabecera(pdf):
		#Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
		archivo_imagen ='nombre_empresa.png'
		#Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
		pdf.drawImage(archivo_imagen, 40, 500, 50, 10,preserveAspectRatio=True) 
         

def tablaExcavadora(pdf,y, obra):
	

    #Creamos una tupla de encabezados para neustra tabla
	encabezados = ('Nº serie','Patente', 'Modelo','Operador', 'Horas diarias', 'Operación Real','Relentis','Consumo Combustible','Rendimiento Promedio', 'Rendimiento Cial')

	fecha_actual = date.today() - timedelta(days=1)
	fechita = '14/02/2017'
	date_object = datetime.strptime(fechita, '%d/%m/%Y').strftime('%Y-%m-%d')
	print date_object.replace('Hrs.','');
	equipo_excavadora = Equipo.objects.filter(Modelo_equipo =('1','2','3') , obra = obra).select_related()

	detalles =[(equipo.equipo.serie_equipo,equipo.equipo.patente_equipo,equipo.equipo.Modelo_equipo.descripcion_modelo,equipo.equipo.chofer.nombre_chofer,
		equipo.hora_diaria,equipo.operacion_real,equipo.relentis,equipo.consumo_combustible,equipo.rendimiento_promedio,equipo.equipo.rendimiento)for equipo in Operacion.objects.filter(fecha = fecha_actual , equipo__obra = obra).exclude(equipo__Modelo_equipo__nombre_modelo = 'WB97R-5E0')]
	detalle_orden = Table([encabezados] + detalles)
	contador = 0
	for detalle in detalles:
		print detalle[4]
		contador = contador + 1
		print contador
		if detalle[4] < 5.6:

			detalle_orden.setStyle(TableStyle(
		        [
		           
		            ('BACKGROUND', (4, contador), (4,contador), colors.red),
		        ]
		    ))
		if detalle[6] > 1.5:
			detalle_orden.setStyle(TableStyle(
		        [
		           ('BACKGROUND', (6, contador), (6,contador), colors.red),
		           
		        ]
		    ))
		if detalle[8] > detalle[9]:
			detalle_orden.setStyle(TableStyle(
		        [
		           ('BACKGROUND', (8, contador), (8,contador), colors.red),
		           
		        ]
		    ))

			    
	detalle_orden.setStyle(TableStyle(
		        [
		            #La primera fila(encabezados) va a estar centrada
		            ('ALIGN',(0,0),(-1,-1),'CENTER'),
		            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
		            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
		            #El tamaño de las letras de cada una de las celdas será de 10
		            ('FONTSIZE', (0, 0), (-1, -1), 9),

		            ('BACKGROUND', (0, 0), (-1, 0), colors.cyan),
		        ]
		    ))		

	#detalles =[(equipo.serie_equipo,equipo.patente_equipo,equipo.Modelo_equipo,equipo.chofer.nombre_chofer,,)for equipo in Equipo.objects.all().select_related()]
	
	
    #Establecemos el tamaño de la hoja que ocupará la tabla 
	detalle_orden.wrapOn(pdf, 800, 600)
    #Definimos la coordenada donde se dibujará la tabla
	detalle_orden.drawOn(pdf, 25,y)
def Tabla(pdf,p):
	
	encabezados1 = ('')
	

	detalle = Table([encabezados1])
	
			    
	detalle.setStyle(TableStyle(
        [
         	('BOX', (0, 0), (-1, 0), 0.25, colors.black),
         	('INERGRID', (0,0),(-1,-1),0.1, colors.black),
            ('BACKGROUND', (-1, 0), (-1, 0), colors.red),
        ]
    ))
   	detalle.wrapOn(pdf, 700, 800)
	detalle.drawOn(pdf,43,p)

def TablaRetro(pdf,y, obra):
	RetroExcavadoras = Equipo.objects.filter(Modelo_equipo ='4' , obra = obra )

	fecha_actual = date.today() - timedelta(days=1)
	encabezados = ('Nº serie','Patente', 'Modelo','Operador', 'Horas diarias')
	
	
	detalles =[(equipo.equipo.serie_equipo,equipo.equipo.patente_equipo,equipo.equipo.Modelo_equipo.descripcion_modelo,equipo.equipo.chofer.nombre_chofer,
			equipo.hora_diaria)for equipo in Operacion.objects.filter(fecha = fecha_actual ,equipo__obra = obra , equipo__Modelo_equipo__nombre_modelo = 'WB97R-5E0')]
	
	detalle_orden = Table([encabezados] + detalles)
	
	contador = 0
	for detalle in detalles:
		print detalle[4]
		contador = contador + 1
		print contador
		if detalle[4] < 5.6:

			detalle_orden.setStyle(TableStyle(
		        [
		           
		            ('BACKGROUND', (4, contador), (4,contador), colors.red),
		        ]
		    ))
		else:
			detalle_orden.setStyle(TableStyle(
		        [
		           
		           
		        ]
		    ))
			    
	detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 10),

            ('BACKGROUND', (0, 0), (-1, 0), colors.cyan),
        ]
    ))
    #Establecemos el tamaño de la hoja que ocupará la tabla 
	detalle_orden.wrapOn(pdf, 700, 800)
    #Definimos la coordenada donde se dibujará la tabla
	
	detalle_orden.drawOn(pdf, 50,y)

def some_view(request, obra):
	obras = Obra.objects.filter(id = obra).select_related()
	
	response = HttpResponse(content_type='application/pdf')
	fecha_actual = date.today() - timedelta(days=1)
	for series in obras:
	
		response['Content-Disposition'] = 'attachment; filename= Obra '+ series.nombre_obra + " "+unicode(fecha_actual.strftime("%d/%m/%Y"))+'.pdf'
	
	temp = StringIO()
	fecha_actual = date.today() - timedelta(days=1)
	
	pdf = canvas.Canvas(temp)
	pdf.setPageSize(landscape(letter))
	print "obra:"
	print obras
	#Dibujamos una cadena en la ubicación X,Y especificada
	
	if obra == '1':
		pdf.setFont("Helvetica", 22)
		pdf.drawString(250, 570, u"Obra Paillaco" + " "+unicode(fecha_actual.strftime("%d/%m/%Y")))
		pdf.setFont("Helvetica", 18)
		pdf.drawString(235, 540, u"Excavadoras Hidráulicas")
		pdf.setFont("Helvetica", 13)
		p=232
		Tabla(pdf,p)
		pdf.drawString(45, 254, u"*: El rendimiento promedio cial , corresponde a los de la semana anterior")
		pdf.drawString(48, 235, u"   Incumplimiento Horas diarias, Relentis y Rendimiento mayor")
		y = 290
		tablaExcavadora(pdf, y, obra)
		#cabecera(pdf)
		pdf.showPage()
		pdf.setPageSize(landscape(letter))
		pdf.setFont("Helvetica", 18)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.drawString(230, 570, u"RetroExcavadoras")
		pdf.setFont("Helvetica", 13)
		p= 380
		Tabla(pdf,p)
		pdf.drawString(48, 383, u"   Incumplimiento Horas diarias, Relentis y Rendimiento mayor")

		y = 440
		TablaRetro(pdf,y, obra )
		pdf.showPage()
	if obra == '2':
		pdf.setFont("Helvetica", 22)
		pdf.drawString(230, 570, u"Obra Los angeles" + " "+unicode(fecha_actual.strftime("%d/%m/%Y")))
		pdf.setFont("Helvetica", 18)
		pdf.drawString(235, 400, u"Excavadoras Hidráulicas")
		pdf.setFont("Helvetica", 13)
		p = 300
		Tabla(pdf,p)
		pdf.drawString(45, 322, u"*: El rendimiento promedio cial , corresponde a los de la semana anterior")
		pdf.drawString(48, 303, u"   Incumplimiento Horas diarias, Relentis y Rendimiento mayor")
		y = 350
		tablaExcavadora(pdf, y, obra)
		#cabecera(pdf)
		pdf.setPageSize(landscape(letter))
		pdf.setFont("Helvetica", 18)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.drawString(230, 530, u"RetroExcavadoras")
		
		y = 450
		TablaRetro(pdf,y, obra )
		pdf.showPage()
	if obra == '3':
		pdf.setFont("Helvetica", 22)
		pdf.drawString(230, 570, u"Obra Tranapuente" + " "+unicode(fecha_actual.strftime("%d/%m/%Y")))
		pdf.setFont("Helvetica", 18)
		pdf.drawString(235, 540, u"Excavadoras Hidráulicas")
		pdf.setFont("Helvetica", 13)
		p = 440
		Tabla(pdf,p)
		pdf.drawString(45, 462, u"*: El rendimiento promedio cial , corresponde a los de la semana anterior")
		pdf.drawString(48, 443, u"   Incumplimiento Horas diarias, Relentis y Rendimiento mayor")
		y = 490
		tablaExcavadora(pdf, y, obra)
		#cabecera(pdf)
		pdf.setPageSize(landscape(letter))
		pdf.showPage()
	if obra == '4':
		pdf.setFont("Helvetica", 22)
		pdf.drawString(230, 570, u"Obra Serviu - Pto saavedra" + " "+unicode(fecha_actual.strftime("%d/%m/%Y")))
		
		pdf.setPageSize(landscape(letter))
		pdf.setFont("Helvetica", 18)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.drawString(230, 530, u"RetroExcavadoras")
		p = 410
		Tabla(pdf,p)
		pdf.drawString(48, 412, u"   Incumplimiento Horas diarias")
		y = 450
		TablaRetro(pdf,y, obra )
		pdf.showPage()
	if obra == '5':
		pdf.setFont("Helvetica", 22)
		pdf.drawString(230, 570, u"Obra Serviu - Renaico" + " "+unicode(fecha_actual.strftime("%d/%m/%Y")))
		pdf.setPageSize(landscape(letter))
		pdf.setFont("Helvetica", 18)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.drawString(230, 530, u"RetroExcavadoras")
		p = 420
		Tabla(pdf,p)
		pdf.drawString(48, 423, u"   Incumplimiento Horas diarias")
		y = 450
		TablaRetro(pdf,y, obra )
		pdf.showPage()

	if obra == '6':
		pdf.setFont("Helvetica", 22)
		pdf.drawString(230, 570, u"Obra Empalme Hinca Tco" + " "+unicode(fecha_actual.strftime("%d/%m/%Y")))
		pdf.setPageSize(landscape(letter))
		pdf.setFont("Helvetica", 18)
		#Dibujamos una cadena en la ubicación X,Y especificada
		pdf.drawString(230, 530, u"RetroExcavadoras")
		p = 420
		Tabla(pdf,p)
		pdf.drawString(48, 422, u"   Incumplimiento Horas diarias")
		y = 450
		TablaRetro(pdf,y, obra )
		pdf.showPage()

	pdf.save()

	response.write(temp.getvalue())
	return response

def hora_entel():
	
	suma_total =0
	datos_serie1 	     = []
	datos_serie2 	     = []
	modelo2      	     = '2017-02-01'
	equipo_excavadora1    = Maquina.objects.values('fecha','movil','patente')
	equipo_excavadora1.query.group_by = ['fecha']
	for datos1 in equipo_excavadora1:
		datos_serie2.append(datos1)

	for datos in datos_serie2:
		suma_dia = 0
		equipo_excavadora    = Maquina.objects.filter(fecha = datos['fecha'] , evento = 'Encendido Motor', patente =datos['patente']).order_by('hora')
		equipo_excavadora2   = Maquina.objects.filter(fecha = datos['fecha'], evento = 'Apagado Motor',patente =datos['patente']).order_by('hora')
		
		
		for series ,series2 in zip(equipo_excavadora ,equipo_excavadora2):
			resta = Decimal(series2.hora) - Decimal(series.hora)
			print resta

		 	suma_dia = suma_dia + resta 
		 	print suma_dia
		 	suma_total = resta + suma_total

		datos_serie1.append(str(suma_dia))
		
		try: 
			obj = Operacion_maq_dia.objects.get( patente = datos['patente'] , mes = datos['fecha'])
			
		except Operacion_maq_dia.DoesNotExist:

			Operacion_maq_dia.objects.create(hora = suma_dia, patente = datos['patente'], Modelo = datos['movil'] , mes = datos['fecha'])


	return datos_serie1

def TablaMaquina(pdf,y):
	
	datos_serie2 = []
	list = []
	equipo_excavadora1    = Maquina.objects.values('fecha')
	equipo_excavadora1.query.group_by = ['fecha']
	for datos1 in equipo_excavadora1:
		list.append(hora_entel())

	equipo_excavadora1    = Maquina.objects.values('fecha','movil','patente')
	equipo_excavadora1.query.group_by = ['fecha']
	for datos1 in equipo_excavadora1:
		datos_serie2.append(datos1)	
		
	detalles =[(maquina['fecha'],maquina['patente'],maquina['movil'],maquina2)for maquina , maquina2 in zip(datos_serie2,list)]

	encabezados = ('Movil','Patente', 'fecha','horas diarias')
	detalle_orden = Table([encabezados] + detalles)
	detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black), 
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]
    ))
    #Establecemos el tamaño de la hoja que ocupará la tabla 
	detalle_orden.wrapOn(pdf, 600, 800)
    #Definimos la coordenada donde se dibujará la tabla
	detalle_orden.drawOn(pdf, 40,y)

def some_view1(request):

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=hello.pdf'
	temp = StringIO()
	fecha_actual = date.today() - timedelta(days=1)
    
	pdf = canvas.Canvas(temp)
	pdf.setPageSize(landscape(letter))
	pdf.setFont("Helvetica", 14)

	#Dibujamos una cadena en la ubicación X,Y especificada
	pdf.setFont("Helvetica", 18)
	pdf.drawString(230, 570, u"Obra Paillaco")
	y = 300
	x= 500
	TablaMaquina(pdf, y)
	#cabecera(pdf)
	pdf.showPage()
	pdf.save()

	response.write(temp.getvalue())
	return response

def create_powerpoint():

	from datetime import datetime
	import xlsxwriter

	datos_serie2 = []
	list_1 = []
	equipo_excavadora1    = Operacion_maq_dia.objects.values('mes','Modelo','patente', 'hora')
	equipo_excavadora1.query.group_by = ['patente']
	for datos1 in equipo_excavadora1:
		datos_serie2.append(datos1)
		
		

	encabezados = ('Movil','Patente', 'fecha','horas diarias')


	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook('Expenses03.xlsx')
	worksheet = workbook.add_worksheet()

	# Add a bold format to use to highlight cells.
	bold = workbook.add_format({'bold': 1})

	# Add a number format for cells with money.
	money_format = workbook.add_format({'num_format': '#,##0'})

	# Add an Excel date format.
	date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

	# Adjust the column width.
	worksheet.set_column(1, 1, 15)
	# Write some data headers.
	worksheet.write('A1', 'Item', bold)
	worksheet.write('B1', 'Date', bold)
	worksheet.write('C1', 'Cost', bold)

	# Some data we want to write to the worksheet.

	# Start from the first cell below the headers.
	row = 1
	col = 0

	for maquina  in datos_serie2:
	    # Convert the date string into a datetime object.

	    worksheet.write_string  (row, col, maquina['Modelo'])
	    worksheet.write_string  (row, col + 1, maquina['patente'])
	    worksheet.write_number  (row, col + 2, maquina['hora'] )
	    worksheet.write_string  (row, col + 3, maquina['mes'] )
	    row += 1

	# Write a total using a formula.

	workbook.close()
	