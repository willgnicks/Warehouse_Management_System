from django.urls import path
from reception_manage import views

app_name = 'receptions_related'
urlpatterns = [
    path('new/', views.add_reception, name='add_reception'),
    path('', views.get_all_receptions, name='all_reception_details'),
]
