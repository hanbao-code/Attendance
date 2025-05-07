from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import DailyAttendance

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def punch_clock(request):
    """
    考勤打卡接口
    根据用户当日打卡次数自动判断为签到或签退
    """
    user = request.user
    today = timezone.now().date()

    # 获取或创建当天的考勤记录
    attendance, created = DailyAttendance.objects.get_or_create(
        user=user,
        date=today,
        defaults={'check_in_time': timezone.now()}
    )

    if not created:
        if attendance.check_in_time is None:
            attendance.check_in_time = timezone.now()
        elif attendance.check_out_time is None:
            attendance.check_out_time = timezone.now()
        else:
            return Response({
                'error': '今日已完整打卡，无法继续操作'
            }, status=400)
        attendance.save()

    return Response({
        'message': '打卡成功',
        'attendance_id': attendance.id,
        'check_in_time': attendance.check_in_time,
        'check_out_time': attendance.check_out_time
    })

# Create your views here.
