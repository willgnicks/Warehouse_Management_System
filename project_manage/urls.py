from django.urls import path
from project_manage import views

# 项目URL
app_name = 'project_related'
urlpatterns = [
    path('', views.get_all_projects, name='all_project_details'),
    path('POST/', views.add_project, name='add_project'),
    path('DELETE/<int:pk>', views.delete_project, name='delete_project'),
    path('GET/', views.get_query_projects, name='get_query_project'),
    path('<int:pk>/', views.get_one_project, name='get_one_project'),
]
