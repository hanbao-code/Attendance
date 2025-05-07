from django.db import models
from Coreuser.models import Coreuser
from django.utils import timezone
import datetime

class DailyAttendance(models.Model):
    user = models.ForeignKey(
        Coreuser,
        on_delete=models.CASCADE,
        verbose_name='用户名称',
        help_text='关联到Coreuser模型的用户信息'
    )
    check_in_time = models.DateTimeField(
        verbose_name='签到时间',
        help_text='当日中第一次签到时记录的时间',
        null=True,
        blank=True
    )
    check_out_time = models.DateTimeField(
        verbose_name='签退时间',
        help_text='当日中第二次签到时记录的时间',
        null=True,
        blank=True
    )
    date = models.DateField(
        verbose_name='日期',
        help_text='考勤记录的日期'
    )
    status = models.CharField(
        max_length=20,
        verbose_name='考勤状态',
        help_text='根据考勤规则自动计算的状态：正常、迟到、早退、旷工半天、全勤等',
        default='未打卡'
    )
    location = models.CharField(
        max_length=255,
        verbose_name='打卡地点',
        help_text='如：总部A区闸机',
        blank=True,
        null=True
    )  # 新增字段

    def save(self, *args, **kwargs):
        if self.check_in_time and self.check_out_time:
            try:
                from Atten.models import AttendanceRule  # 延迟导入以避免循环依赖
                rule = AttendanceRule.objects.get(user=self.user)
                on_duty = datetime.datetime.combine(self.date, rule.on_duty_time)
                off_duty = datetime.datetime.combine(self.date, rule.off_duty_time)
                late_limit = on_duty + datetime.timedelta(minutes=rule.late_threshold)
                early_limit = off_duty - datetime.timedelta(minutes=rule.early_threshold)

                is_late = self.check_in_time > late_limit
                is_early = self.check_out_time < early_limit

                if is_late and is_early:
                    self.status = '旷工半天'
                elif is_late:
                    self.status = '迟到'
                elif is_early:
                    self.status = '早退'
                else:
                    self.status = '正常'
            except AttendanceRule.DoesNotExist:
                self.status = '无考勤规则'
        elif self.check_in_time or self.check_out_time:
            self.status = '打卡不完整'
        else:
            self.status = '未打卡'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.name} - {self.date}'

    class Meta:
        verbose_name = '日考勤'
        verbose_name_plural = '日考勤'

class AttendanceRule(models.Model):
    user = models.OneToOneField(
        Coreuser,
        on_delete=models.CASCADE,
        verbose_name='用户名称',
        help_text='关联到Coreuser模型的用户信息'
    )
    on_duty_time = models.TimeField(
        verbose_name='到岗时间',
        help_text='默认早上9点',
        default='09:00:00'
    )
    off_duty_time = models.TimeField(
        verbose_name='下岗时间',
        help_text='默认下午6点',
        default='18:00:00'
    )
    working_hours = models.FloatField(
        verbose_name='当日工时',
        help_text='默认8小时',
        default=8.0
    )
    late_threshold = models.IntegerField(
        verbose_name='迟到阈值',
        help_text='默认30分钟',
        default=30
    )
    early_threshold = models.IntegerField(
        verbose_name='早退阈值',
        help_text='默认30分钟',
        default=30
    )

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = '考勤规则'
        verbose_name_plural = '考勤规则'

class MonthlyAttendance(models.Model):
    user = models.ForeignKey(
        Coreuser,
        on_delete=models.CASCADE,
        verbose_name='用户名称',
        help_text='关联到Coreuser模型的用户信息'
    )
    work_days = models.IntegerField(
        verbose_name='工作天数',
        help_text='默认为0',
        default=0
    )
    month = models.DateField(
        verbose_name='月份',
        help_text='考勤记录的月份'
    )

    def __str__(self):
        return f'{self.user.name} - {self.month.strftime("%Y-%m")}'

    class Meta:
        verbose_name = '月考勤'
        verbose_name_plural = '月考勤'