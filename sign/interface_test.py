import requests
import unittest

'''# 查询发布会接口
url = "http://127.0.0.1:8000/api/get_event_list/"
r = requests.get(url, params={'eid': '2'})
result = r.json()

# 断言接口返回值
assert result['status'] == 200
assert result['message'] == 'success'
assert result['data']['name'] == '柔柔弱弱'
assert result['data']['address'] == '江苏省南京市玄武区会议中心'
assert result['data']['start_time'] == '2018-08-15T06:00:00Z'''''


class GetEventListTest(unittest.TestCase):
    '''查询发布会接口测试'''

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'

    def test_get_event_null(self):
        '''发布会ID为空'''

        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], 'parameter error')

    def test_get_event_error(self):
        '''发布会ID不存在'''

        r = requests.get(self.url, params={'eid': '902'})
        result = r.json()
        self.assertEqual(result['status'], 10022)
        self.assertEqual(result['message'], 'query result is empty')

    def test_get_event_success(self):
        '''发布会ID为2，查询成功'''

        r = requests.get(self.url, params={'eid': '2'})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '柔柔弱弱')
        self.assertEqual(result['data']['address'], '江苏省南京市玄武区会议中心')
        self.assertEqual(result['data']['start_time'], '2018-08-15T06:00:00Z')


if __name__ == '__main__':
    unittest.main()
