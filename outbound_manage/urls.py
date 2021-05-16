from django.urls import path
from outbound_manage import views
app_name = 'outbound_related'
urlpatterns = [
    path('POST/', views.add_outbound, name='add_outbound'),
    path('', views.get_all_outbounds, name='all_outbound_details'),
]
