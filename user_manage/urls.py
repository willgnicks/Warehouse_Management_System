from django.urls import path, re_path
from user_manage import views

# 用户管理路由
app_name = 'user_related'
urlpatterns = [
    path('', views.get_all_users, name='all_users_details'),
    path('<int:pk>/', views.get_all_users, name='specify_user_details', ),
    path('DELETE/<int:pk>', views.delete_user, name='delete_user'),
    path('POST/', views.add_user, name='add_user'),

    # path('delete/', views.delete_user),
    # path('update/', views.update_user),

]
