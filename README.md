# manager-server

# 安装方法：

## 服务端安装
### 下载

``` bash
$git clone https://github.com/t880216t/manager-server.git
```

### 安装依赖模块
``` bash
$pip install -r requirements.txt
```

其中有mysql-db可以再这里下载：https://sourceforge.net/projects/mysql-python/?source=directory
如果对应的版本不对请百度找下。

## 数据库结构导入

安装MYSQL，新建个库。
数据库工具导入文件‘tables.sql’。

##服务端配置数据库

编辑文件‘manager-server/app/database_config.py’
``` bash
database_host = "127.0.0.1"#你的数据库地址
database_username = "root"#数据库的登录账号
database_password = "root"#数据库的登录账号
database1 = "1"#放项目数据的数据库名
database2 = "2"#不用配置
```

## 服务端启动

本项目根目录
``` bash
$python run.py
```
默认的地址：http://127.0.0.1:5000/
