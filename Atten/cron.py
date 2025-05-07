from django.core.management import call_command
from django_cron import CronJobBase, Schedule

class UpdateMonthlyAttendanceCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # 每天凌晨执行

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'atten.update_monthly_attendance'

    def do(self):
        call_command('update_monthly_attendance')