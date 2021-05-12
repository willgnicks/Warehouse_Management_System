from django.urls import path
from purchase_manage import views

app_name = 'purchase_related'
urlpatterns = [
    path('', views.get_all_purchases, name='all_purchase_details'),
    path('purchase/', views.add_purchase, name='add_purchase'),
    path('<int:pk>/', views.get_and_update, name='get_and_update_purchase'),
    path('<str:keyword>/', views.check_occupy, name='check_occupy'),
]
