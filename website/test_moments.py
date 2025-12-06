import unittest
import os
from app import app

class TestMomentsPage(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for something on home page to verify
        self.assertIn(b'particles-js', response.data)

    def test_moments_page_exists(self):
        response = self.client.get('/moments')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("柔光摇篮", content)
        self.assertIn("孕妈情绪安抚与助眠伴侣", content)
        self.assertIn("support@anyong.cn", content)

    def test_moments_page_slash(self):
        response = self.client.get('/moments/')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("柔光摇篮", content)

    def test_moments_policy_page_exists(self):
        response = self.client.get('/moments/policy')
        self.assertEqual(response.status_code, 200)
        content = response.data.decode('utf-8')
        self.assertIn("隐私政策", content)
        self.assertIn("信息收集", content)
        # Check for key phrases that exist in the HTML
        self.assertIn("个人身份信息", content)
        self.assertIn("不会", content)

    def test_caching_headers_html(self):
        response = self.client.get('/moments')
        self.assertEqual(response.status_code, 200)
        cache_control = response.headers.get('Cache-Control')
        self.assertIn("max-age=3600", cache_control)

    def test_caching_headers_assets(self):
        # Request styles.css which should exist in root
        response = self.client.get('/styles.css')
        self.assertEqual(response.status_code, 200)
        cache_control = response.headers.get('Cache-Control')
        self.assertIn("max-age=86400", cache_control)

if __name__ == '__main__':
    unittest.main()
