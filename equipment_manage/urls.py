from django.urls import path
from equipment_manage import views

app_name = 'equipment_related'
urlpatterns = [
    path('', views.get_all_equips, name='get_all_equips')

]
