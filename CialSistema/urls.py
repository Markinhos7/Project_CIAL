from django.conf.urls import include, url
from. import views

urlpatterns = [

	 #url(r'^$', views.post_list),
	 url(r'index/(\d+)$',views.some_view),
	 url(r'^$',views.GeneratePdf),
	 url(r'index2/',views.post_list),
]
