from django.urls import path
from inbound_manage import views

app_name = 'inbound_related'
urlpatterns = [
    path('POST/', views.add_or_update, name='add_or_update'),
    path('get_rel/', views.get_rel, name='get_rel'),
    path('', views.get_all_inbounds, name='all_inbounds_details'),
    path('<int:pk>/', views.get_one, name='get_one_inbound'),
    path('DELETE/<int:pk>', views.delete_one, name='delete_inbound'),
    path('GET/', views.get_query_inbound, name='get_query_inbound'),
    path('GET/<str:query>/', views.check_occupy, name='check_occupy'),
]
