from django.urls import path
from product_manage import views

# 项目URL
app_name = 'product_related'
urlpatterns = [
    path('', views.get_all_products, name='all_product_details'),
    path('new/', views.add_product, name='add_product'),
    path('DELETE/<int:pk>', views.delete_product, name='delete_product'),
    path('GET/', views.ajax_all_products, name='ajax_products'),
]
