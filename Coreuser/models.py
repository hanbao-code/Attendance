# Coreuser/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Coreuser(AbstractUser):
    # 用户名和密码继承自AbstractUser
    ROLE_CHOICES = (
        (1, '员工'),
        (2, '部门经理'),
        (3, '人事管理'),
    )
    role = models.IntegerField(
        choices=ROLE_CHOICES,
        default=1,
        verbose_name='用户角色',
        help_text='1-员工，2-部门经理，3-人事管理'
    )
    is_super_admin = models.BooleanField(
        default=False,
        verbose_name='是否超级管理员',
        help_text='指定用户是否为超级管理员，拥有最高权限'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='姓名',
        help_text='用户的中文全名'
    )
    email = models.EmailField(
        verbose_name='邮箱',
        help_text='用户的电子邮箱地址'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='电话',
        help_text='用户的联系电话号码'
    )
    department = models.CharField(
        max_length=100,
        verbose_name='部门',
        help_text='用户所属的公司部门或团队'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='用户账户创建的日期和时间'
    )

    # 解决与默认User模型的反向访问器冲突
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='用户组',
        help_text='用户所属的权限组',
        blank=True,
        related_name='coreuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='用户权限',
        help_text='用户拥有的特定权限',
        blank=True,
        related_name='coreuser_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'