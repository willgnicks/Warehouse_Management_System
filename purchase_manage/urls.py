from django.urls import path
from purchase_manage import views

app_name = 'purchase_related'
urlpatterns = [
    path('', views.get_all_purchases, name='all_purchase_details'),
    path('POST/', views.add_or_update, name='add_or_update'),
    path('DELETE/<int:pk>', views.delete_one, name='delete_purchase'),
    path('<int:pk>/', views.get_one, name='get_one_purchase'),
    path('GET/', views.get_query_purchase, name='get_query_purchase'),
    path('GET/<str:query>/', views.check_occupy, name='check_occupy'),
]
