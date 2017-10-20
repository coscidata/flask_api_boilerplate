# app

![pyversions](https://img.shields.io/badge/python%20-3.6%2B-blue.svg)

## 开发

### 安装依赖

```shell
pip install -r requirements-dev.txt
```

### 创建数据库

```mysql
CREATE DATABASE `{db_name}` DEFAULT CHARACTER SET = `utf8mb4`;
```

### ORM 管理数据库

```shell
# 只有第一次需要使用
python manage.py db init
# 检查 model 是否更新
python manage.py db migrate
# 更新数据库
python manage.py db upgrade
```

### 运行

配置相关环境变量

```shell
cp seattle/local_config.py.template seattle/local_config.py
```

运行

```shell
python run.py
```

### 格式化代码

```shell
sh tools/format_python_code.sh
```
