# Coreuser/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoreuserViewSet, register, login, check_login_status

router = DefaultRouter()
# 注释掉原有的users路由注册
# router.register(r'users', CoreuserViewSet)

urlpatterns = [
    # 注释掉原有的users路径
    # path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('check-login/', check_login_status, name='check_login_status'),
]