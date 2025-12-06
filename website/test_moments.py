import unittest
import threading
import http.server
import socketserver
import urllib.request
import time
import os
from app import CustomHandler

PORT = 8999
BASE_URL = f"http://localhost:{PORT}"

class TestMomentsPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set directory to website root
        web_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(web_dir)
        
        cls.httpd = socketserver.TCPServer(("", PORT), CustomHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1) # Give it a moment to start

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_moments_page_exists(self):
        url = f"{BASE_URL}/moments/"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            content = response.read().decode('utf-8')
            self.assertIn("柔光摇篮", content)
            self.assertIn("孕妈情绪安抚与助眠伴侣", content)
            self.assertIn("support@anyong.cn", content)

    def test_caching_headers_html(self):
        url = f"{BASE_URL}/moments/"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            cache_control = response.headers.get('Cache-Control')
            self.assertIn("max-age=3600", cache_control)

    def test_caching_headers_assets(self):
        # Assuming there is a css file or we can request one, 
        # but let's just check the logic by requesting a fake css
        # Note: SimpleHTTPRequestHandler returns 404 for missing files but headers might still be set if we were intercepting earlier.
        # However, CustomHandler calls super().end_headers() which sends headers. 
        # But for 404, SimpleHTTPRequestHandler sends error. 
        # Let's request the existing styles.css
        url = f"{BASE_URL}/styles.css"
        with urllib.request.urlopen(url) as response:
            self.assertEqual(response.status, 200)
            cache_control = response.headers.get('Cache-Control')
            self.assertIn("max-age=86400", cache_control)

if __name__ == '__main__':
    unittest.main()
