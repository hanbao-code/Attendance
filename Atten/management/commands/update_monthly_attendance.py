import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from Atten.models import DailyAttendance, MonthlyAttendance

class Command(BaseCommand):
    help = '将上个月的日考勤数据汇总到月考勤表中'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        last_month = (first_day_of_month - datetime.timedelta(days=1)).replace(day=1)
        next_month = (last_month + datetime.timedelta(days=32)).replace(day=1)

        users = DailyAttendance.objects.values_list('user', flat=True).distinct()

        for user_id in users:
            # 计算用户上个月的有效工作天数
            work_days = DailyAttendance.objects.filter(
                user_id=user_id,
                date__gte=last_month,
                date__lt=next_month,
                status='正常'
            ).count()

            # 更新或创建 MonthlyAttendance 记录
            MonthlyAttendance.objects.update_or_create(
                user_id=user_id,
                month=last_month,
                defaults={'work_days': work_days}
            )

            self.stdout.write(self.style.SUCCESS(f'成功更新用户 {user_id} 的月考勤记录'))