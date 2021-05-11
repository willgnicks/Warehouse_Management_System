from django.urls import path
from manufacturer_manage import views

app_name = 'manufacturer-related'
urlpatterns = [
    path('new/', views.add_manufacturer, name='add_manufacturer'),
    path('', views.get_all_manufacturers, name='all_manufacturer_details'),
]
