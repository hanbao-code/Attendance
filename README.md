# 考勤管理系统

## 项目说明
本项目为基于Django框架开发的考勤管理系统，包含用户认证、每日考勤记录和月度统计功能。

## 开发环境
- Python 3.10+
- Django 4.2+
- SQLite 数据库

## 快速启动
```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 功能模块
1. 用户管理（Coreuser应用）：支持部门、角色管理
2. 考勤记录（Atten应用）：包含每日打卡、异常处理
3. 后台管理界面：提供数据可视化看板

## 代码规范
- 遵循PEP8编码规范
- 使用DRY/KISS设计原则
- ORM操作使用Django原生方法
- 推荐使用`black`和`flake8`进行代码格式检查



## 文档更新
1. API接口文档请参考[docs/api.md]
2. 数据模型ER图请参考[docs/er_diagram.md]