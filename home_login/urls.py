from django.urls import path, re_path
from home_login import views

# 路由
app_name = 'home_and_login'
urlpatterns = [
    path('', views.login, name='go_login'),
    # path('<status>', views.login, name='go_login'),
    path('middle/', views.go_add_session_key, name='go_add_session_key'),
    re_path(r'home/$', views.go_home, name='go_home'),
    # path('valid/', views.valid_user, name='verify_status'),
    path('logout/', views.logout),

]
