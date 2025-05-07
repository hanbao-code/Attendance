from django.contrib import admin
from Atten.models import DailyAttendance, AttendanceRule, MonthlyAttendance
from django.utils.html import format_html

class DailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'check_in_time', 'check_out_time', 'status', 'get_status_color')
    list_filter = ('date', 'user', 'status')
    search_fields = ('user__username',)
    readonly_fields = ('date', 'check_in_time', 'check_out_time', 'status')
    change_list_template = 'admin/atten/dailyattendance/change_list.html'  # 使用自定义模板

    def get_status_color(self, obj):
        status_colors = {
            '正常': 'green',
            '迟到': 'orange',
            '早退': 'blue',
            '旷工半天': 'red',
            '未打卡': 'gray',
            '打卡不完整': 'brown',
            '无考勤规则': 'purple'
        }
        return format_html(
            '<span class="status-{}">{}</span>',
            obj.status.replace(' ', '').lower(),
            obj.status
        )

    get_status_color.short_description = '状态'

    def has_add_permission(self, request):
        return False  # 禁止手动添加日考勤记录

@admin.register(AttendanceRule)
class AttendanceRuleAdmin(admin.ModelAdmin):
    list_display = ('user', 'on_duty_time', 'off_duty_time', 'working_hours')
    list_filter = ('user',)
    search_fields = ('user__username',)
    readonly_fields = ('user',)

    def has_delete_permission(self, request, obj=None):
        return False  # 禁止删除考勤规则

@admin.register(MonthlyAttendance)
class MonthlyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'work_days')
    list_filter = ('month', 'user')
    search_fields = ('user__username',)
    readonly_fields = ('month', 'work_days')

    def has_change_permission(self, request, obj=None):
        return False  # 禁止手动修改月考勤数据

# Register your models here.
