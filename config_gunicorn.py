# nohup gunicorn -c config_gunicorn.py mini:app &
import multiprocessing

# 是否开启debug模式
debug = True
# 访问地址
bind = "0.0.0.0:8000"
# 工作进程数 Gunicorn官方推荐的配置是CPU数量×2+1
workers = multiprocessing.cpu_count() * 2 + 1
# 工作线程数
threads = multiprocessing.cpu_count()
# 超时时间
timeout = 600
# 输出日志级别
loglevel = 'debug'
# 存放日志路径
#pidfile = ".log/gunicorn.pid"
# 存放日志路径
# accesslog = "./log/access.log"
# 存放日志路径
# errorlog = "./log/debug.log"
