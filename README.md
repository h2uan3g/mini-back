mini-back
======

### 功能介绍
- 文档添加水印、预览


### 技术栈
- flask


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
