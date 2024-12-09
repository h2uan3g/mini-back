import unittest
import threading
import re
from app import create_app, db, fake
from app.models import Role, User

from selenium.webdriver.chrome.service import Service

from selenium import webdriver


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # 启动Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            service = Service('/Users/zhuqian/develop/chrome/chrome-mac-x64')
            cls.client = webdriver.Chrome(chrome_options=options, service=service)
        except:
            pass

        # 如果无法启动浏览器，跳过这些测试
        if cls.client:
            # 创建应用
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # 禁止日志，保持输出简洁
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # 创建数据库，并使用一些虚拟数据填充
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # 添加管理员
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com',
                         username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # 在一个线程中启动Flask服务器
            cls.server_thread = threading.Thread(
                target=cls.app.run, kwargs={'debug': 'false',
                                            'use_reloader': False,
                                            'use_debugger': False})
            cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # 关闭Flask服务器和浏览器
            cls.client.get('http://localhost:9001/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            # 销毁数据库
            db.drop_all()
            db.session.remove()

            # 删除应用上下文
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:9001/')
        self.assertTrue(re.search('Hello,\s+Stranger!',
                                  self.client.page_source))

        # navigate to login page
        self.client.find_element_by_link_text('Log In').click()
        self.assertIn('<h1>Login</h1>', self.client.page_source)

        # login
        self.client.find_element_by_name('email'). \
            send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))

        # navigate to the user's profile page
        self.client.find_element_by_link_text('Profile').click()
        self.assertIn('<h1>john</h1>', self.client.page_source)
