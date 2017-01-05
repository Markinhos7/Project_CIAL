from django.conf.urls import include, url
from. import views

urlpatterns = [

	 url(r'^$', views.obtener_titulo),
	 url(r'^index/', views.obtener_equipo),
]
