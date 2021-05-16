from django.urls import path
from consumer_manage import views

# 用户管理路由
app_name = 'consumer_related'
urlpatterns = [
    path('', views.get_all_consumers, name='all_consumers_details'),
    path('DELETE/<int:pk>', views.delete_consumer, name='delete_consumer'),
    path('POST/', views.add_consumer, name='add_consumer'),
    path('GET/', views.get_query_consumers, name='get_query_consumers'),
    path('<int:pk>/', views.get_one_consumer, name='get_one_consumer'),

]
