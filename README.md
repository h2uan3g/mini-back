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
    - 智能问答 (deepseek api 接入)
- 微信接口
    - 获取微信手机号


### 系统截图
![登录](./short/login.png)
![数据大屏](./short/bigscreen.png)
![客户](./short/cusmer.png)
![用户](./short/product.png)
![问答系统](./short/chat.png)
![积分商城](./short/mall.png)




### 技术栈
- flask + jinjia2 + sqllite
- echarts
- 微信接口


### 运行
1. touch .env 设置环境变量   
```bash
# .env
FLASK_APP=mini.py
FLASK_DEBUG=1
FLASKY_ADMIN=admin@example.com
WEIXIN_APPID=xxx        # 替换
WEIXIN_SECRET=xxx       # 替换
DEEPSEEK_APIKEY=xxx     # 替换
```

2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. 运行
```bash
flask run -p 9001
```

### 资料分享
1. 进群送Python、JS入门资料
2. python 资料
    - python原创入门笔记
    - flask学习笔记
    - python 精选书籍
        - 《Python编程：从入门到实践（第2版）》
        - 《流畅的Python（第2版）》
        - 《Effective Python：编写高质量Python代码的90个有效方法（原书第2版）》
3. 前端资料
    - JS 原创入门笔记
    - 前端精选书籍
        - 《JavaScript高级程序设计（第4版）》
        - 《JavaScript语言精髓与编程实践（第3版）》
        - 《CSS世界》
4. 数据库
    - 书籍
        - 《SQL必知必会(第5版)》
5. 线上部署技术指导
    - gunicorn + nginx 线上部署
6. 和十年行业从业者讨论行业方向

