from django_cron import CronJobBase, Schedule
from django.core.management import call_command

class UpdateMonthlyAttendanceCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # 每天凌晨执行

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'atten.update_monthly_attendance'

    def do(self):
        call_command('update_monthly_attendance')


class ClearMonthlyAttendanceCronJob(CronJobBase):
    RUN_AT_TIMES = ['01:00']  # 每日凌晨1点执行

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'atten.clear_monthly_attendance'

    def do(self):
        call_command('clear_monthly_attendance')
