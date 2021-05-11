from django.urls import path
from purchase_manage import views

app_name = 'purchase_related'
urlpatterns = [
    path('POST/', views.add_purchase, name='add_purchase'),
    path('GET/', views.get_all_purchases, name='all_purchase_details'),
]
