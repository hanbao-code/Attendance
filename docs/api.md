# API 接口文档

## 用户管理（Coreuser）
### 获取用户列表
- **URL**: `/api/users/`
- **Method**: `GET`
- **参数**:
  - `department` (可选): 部门ID过滤
  - `role` (可选): 角色类型过滤
- **响应示例**:
```json
[
  {
    "id": 1,
    "username": "zhangsan",
    "department": "技术部",
    "role": "普通用户"
  }
]
```

### 创建用户
- **URL**: `/api/users/`
- **Method**: `POST`
- **请求体**:
```json
{
  "username": "lisi",
  "password": "123456",
  "department": "市场部",
  "role": "admin"
}
```

## 考勤记录（Atten）
### 打卡接口
- **URL**: `/api/attendance/punch/`
- **Method**: `POST`
- **请求体**:
```json
{
  "user_id": 1,
  "location": "总部A区闸机"
}
```
- **响应示例**:
```json
{
  "status": "success",
  "timestamp": "2024-03-20T08:58:32+08:00",
  "location": "总部A区闸机"
}
```

## 认证说明
所有接口需携带JWT Token认证，通过`Authorization: Bearer <token>`头传递