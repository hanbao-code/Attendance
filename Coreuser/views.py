# Coreuser/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from .models import Coreuser
from .serializers import CoreuserSerializer, RegisterSerializer

def register(request):
    """
    用户注册接口
    需要提供用户名、密码和角色
    角色选项：1-员工，2-部门经理，3-人事管理
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': '用户注册成功',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    简单的登录接口（实际应使用DRF的认证机制或JWT）
    需要提供用户名和密码
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': '必须提供用户名和密码'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Coreuser.objects.get(username=username)
    except Coreuser.DoesNotExist:
        return Response({
            'error': '用户名或密码错误'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.check_password(password):
        return Response({
            'error': '用户名或密码错误'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 设置session值，用于标识用户已登录
    request.session['user_id'] = user.id
    request.session['login_time'] = str(timezone.now())  # 将datetime转为字符串存储
    
    # 实际应用中应该返回token而不是简单消息
    return Response({
        'message': '登录成功',
        'user_id': user.id,
        'username': user.username,
        'role': user.role  # 返回用户角色信息
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_login_status(request):
    """
    检查用户登录状态的接口
    如果session中存在user_id且未过期，则认为用户已登录
    """
    user_id = request.session.get('user_id')
    login_time_str = request.session.get('login_time')
    
    if not user_id or not login_time_str:
        return Response({
            'is_logged_in': False,
            'message': '用户未登录或会话已过期'
        })
    
    try:
        user = Coreuser.objects.get(id=user_id)
    except Coreuser.DoesNotExist:
        return Response({
            'is_logged_in': False,
            'message': '用户不存在'
        })
    
    # 计算登录时间是否在有效期内（5分钟）
    login_time = timezone.datetime.fromisoformat(login_time_str.replace('Z', '+00:00'))
    if (timezone.now() - login_time).total_seconds() > 300:  # 5分钟=300秒
        # 清除过期的session
        request.session.flush()
        return Response({
            'is_logged_in': False,
            'message': '会话已过期，请重新登录'
        })
    
    return Response({
        'is_logged_in': True,
        'user_id': user.id,
        'username': user.username,
        'login_time': login_time_str
    })


class CoreuserViewSet(viewsets.ModelViewSet):
    queryset = Coreuser.objects.all()
    serializer_class = CoreuserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 只允许用户查看自己的信息，除非是超级管理员或人事管理
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or getattr(self.request.user, 'is_super_admin', False):
                return Coreuser.objects.all()
            else:
                return Coreuser.objects.filter(id=self.request.user.id)
        return Coreuser.objects.none()

    def perform_create(self, serializer):
        # 确保创建用户时密码被正确加密存储
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data['password'])
            user.save()