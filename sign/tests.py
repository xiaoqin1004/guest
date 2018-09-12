# 导入单元测试框架unittest
from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User


# Create your tests here.
# 创建ModelTest类继承unittest.TestCase类
class ModelTest(TestCase):

    # 测试用例前的初始化工作，例如初始化变量，生成数据库测试数据，打开浏览器等
    def setUp(self):
        # 创建一条发布会和嘉宾数据
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000,
                             address="shenzhen", start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realname='alen', phone='13711001101', email='alen@mail.com', sign=False)

    # 测试方法必须以test开头
    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')      # 查询创建的数据
        self.assertEqual(result.address, "shenzhen")            # 断言数据是否正确
        self.assertTrue(result.status)                          # 断言查询出的发布会数据的状态是否为True

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    ''' 测试index登录首页 '''

    def test_index_page_renders_index_template(self):
        ''' 测试index视图 '''
        response = self.client.get('/index/')           # 通过client.get()方法请求index路径
        self.assertEqual(response.status_code, 200)     # status_code获取HTTP返回的状态码，断言状态码是否为200
        self.assertTemplateUsed(response, 'index.html') # 断言服务器是否用给定的index.html来响应


class LoginActionTest(TestCase):
    '''测试登录动作'''

    # 创建登录用户数据
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    # 用于测试添加的用户数据是否正确
    def test_add_admin(self):
        '''测试添加用户'''
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'admin@mail.com')

    def test_login_action_username_password_null(self):
        '''用户名密码为空'''
        # 定义用户登录参数
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        # assertIn()方法断言返回的HTML页面中是否包含username or password error!提示字符串
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_username_password_error(self):
        '''用户名密码错误'''
        test_data = {'username': 'abc', 'password': '123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_success(self):
        '''登录成功'''
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    '''发布会管理'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="xiaomi5 event", status=1, limit=2000,
                             address="shenzhen", start_time='2016-08-31 06:18:22')
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    def test_event_mange_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'shenzhen', response.content)
        self.assertIn(b'xiaomi5', response.content)
