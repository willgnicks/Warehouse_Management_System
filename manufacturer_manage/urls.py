from django.urls import path
from manufacturer_manage import views

app_name = 'manufacturer_related'
urlpatterns = [
    path('POST/', views.add_manufacturer, name='add_manufacturer'),
    path('', views.get_all_manufacturers, name='all_manufacturer_details'),
    path('<int:pk>/', views.get_one_manufacturer, name='get_one_manufacturer'),
    path('DELETE/<int:pk>', views.delete_manufacturer, name='delete_manufacturer'),
    path('GET/', views.get_query_manufacturers, name='get_query_manufacturers'),
]
