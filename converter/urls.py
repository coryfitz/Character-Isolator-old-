from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin

app_name = 'converter'
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^foo/',views.download, name='download'),
    url(r'^admin/', admin.site.urls),
]
