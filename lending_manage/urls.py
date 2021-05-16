from django.urls import path
from lending_manage import views

app_name = 'lending_related'
urlpatterns = [
    path('POST/', views.add_lending, name='add_lending'),
    path('', views.get_all_lendings, name='all_lending_details'),
]
