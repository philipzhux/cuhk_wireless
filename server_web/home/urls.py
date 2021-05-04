from django.conf.urls import url
from . import views
from django.urls import path
urlpatterns = [url('index', views.index, name='index')
,path('showloc/<int:loc>/', views.httx, name='location')]