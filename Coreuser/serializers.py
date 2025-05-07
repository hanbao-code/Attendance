# Coreuser/serializers.py
from rest_framework import serializers
from .models import Coreuser

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.ChoiceField(choices=[(1, '员工'), (2, '部门经理'), (3, '人事管理')])

    def create(self, validated_data):
        return Coreuser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )


class CoreuserSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField(
        default=1,
        help_text='用户角色：1-员工，2-部门经理，3-人事管理'
    )

    class Meta:
        model = Coreuser
        fields = ['id', 'username', 'password', 'name', 'email', 'phone', 'department', 'role', 'is_super_admin']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': False},  # 允许更新角色
        }

    def create(self, validated_data):
        user = Coreuser(
            username=validated_data['username'],
            name=validated_data.get('name', ''),
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            department=validated_data.get('department', ''),
            role=validated_data.get('role', 1),
            is_super_admin=validated_data.get('is_super_admin', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # 密码单独处理，仅在提供时更新
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
