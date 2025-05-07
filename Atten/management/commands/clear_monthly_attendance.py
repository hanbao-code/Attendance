import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from Atten.models import MonthlyAttendance

class Command(BaseCommand):
    help = '清理月考勤历史数据，保留最近一个月的记录'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        first_day_of_month = today.replace(day=1)
        
        # 计算保留的起始月份（最近一个月）
        keep_date = (first_day_of_month - datetime.timedelta(days=1)).replace(day=1)
        
        try:
            # 删除上个月之前的所有月考勤记录
            MonthlyAttendance.objects.filter(month__lt=keep_date).delete()
            self.stdout.write(self.style.SUCCESS(f'成功清理 {keep_date} 之前的月考勤记录'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'清理月考勤记录失败: {str(e)}'))