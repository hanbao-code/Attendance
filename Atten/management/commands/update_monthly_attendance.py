import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from Atten.models import DailyAttendance, MonthlyAttendance

class Command(BaseCommand):
    help = '将上个月的日考勤数据汇总到月考勤表中'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        yesterday = today - datetime.timedelta(days=1)

        # 先执行月度考勤更新
        users = DailyAttendance.objects.filter(date=yesterday).values_list('user', flat=True).distinct()
        for user_id in users:
            # 计算昨日正常出勤情况
            is_workday = DailyAttendance.objects.filter(
                user_id=user_id,
                date=yesterday,
                status='正常'
            ).exists()

            if is_workday:
                # 获取或创建本月记录
                monthly_record, created = MonthlyAttendance.objects.get_or_create(
                    user_id=user_id,
                    month=yesterday.replace(day=1),
                    defaults={'work_days': 1}
                )

                if not created:
                    # 仅当未创建新记录时才更新
                    monthly_record.work_days += 1
                    monthly_record.save()

                self.stdout.write(self.style.SUCCESS(f'更新用户 {user_id} 的月考勤记录'))

        # 再执行数据清理
        try:
            DailyAttendance.objects.filter(date=yesterday).delete()
            self.stdout.write(self.style.SUCCESS(f'成功清理 {yesterday} 的日考勤记录'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'清理日考勤记录失败: {str(e)}'))
