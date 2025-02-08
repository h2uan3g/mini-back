mini-back
======

### 功能介绍
- 登录、注册、权限管理、用户管理
    - 超级管理员
- 数据分析
    - 数据大屏
    - 数据可视化(图表分析)
- 工作台(图文管理)
    - 图片新闻
    - 图文新闻
- 商城管理
    - 产品管理
    - 积分管理
    - 订单管理
- 合同管理
    - 文档添加水印、预览
- 智能问答系统
    - 智能问答 (deepseek)


### 系统截图


### 技术栈
- flask + nginx
- pychar


### 部署发布
#### 使用 Systemd 管理 Gunicorn
 - `在 /etc/systemd/system/ 目录下创建一个服务文件，例如 flask_app.service`
 ```ini
[Unit]
Description=Gunicorn instance to serve my Flask app
After=network.target

[Service]
User=<你的用户名>
Group=<你的用户组>
WorkingDirectory=/path/to/your/flask/app
ExecStart=nohup gunicorn -c config_gunicorn.py flasky:app &
Restart=always

[Install]
WantedBy=multi-user.target
```
 - `重载配置文件`
 ```bash
 sudo systemctl daemon-reload
 ```
 - `启动服务`
 ```bash
 sudo systemctl start flask_app
 ```
 - `停止服务`
 ```bash
 sudo systemctl stop flask_app
 ```
 #### nginx 配置
 ```nginx
http {
    ...
    
    upstream mini {
        server 127.0.0.1:9000;
        server unix:/tmp/gunicorn.sock;  # Nginx与Gunicorn之间通信的socket文件
    }

    server {
        listen 80;
        server_name 127.0.0.1;
        access_log /tmp/gunicornnginx/access_log;
        error_log /tmp/gunicornnginx/error_log;
        location /favicon.ico {
            root /Users/mini/static/;  # 静态文件的根目录
        }

        location ^~ /static/ {
            root /Users/mini/;              # root  静态文件的根目录
            # alias /Users/mini/static;     # alias  静态文件的根目录
        }

        location / {
            proxy_pass: http://mini;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
 ```

### 设置用户
#### 设置超级管理员
- 1. 变量设置邮件 (注册前设置)
- 2. 在 flasky.py 中执行 `flask deploy --name=admin`



