from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AttenConfig(AppConfig):
    # 设置默认主键类型为BigAutoField（64位整数）
    default_auto_field = 'django.db.models.BigAutoField'
    # 应用的Python路径，需与应用目录名保持一致
    name = 'Atten'

    def ready(self):
        # ready()方法在应用启动时执行，用于初始化代码
        # 原本用于自动发现定时任务模块，但存在版本兼容性问题
        # 已临时禁用，待验证django-cron版本兼容性后再启用
        # django_cron.autodiscover()
        pass  # 暂时代理初始化逻辑