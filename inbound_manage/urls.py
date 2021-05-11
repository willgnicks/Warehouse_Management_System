from django.urls import path
from inbound_manage import views

app_name = 'inbound_related'
urlpatterns = [
    path('new/', views.add_inbound, name='add_inbound'),
    path('', views.get_all_inbounds, name='all_inbounds_details'),
]
