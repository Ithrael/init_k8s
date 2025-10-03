import http.server
import socketserver
import os

# 设置端口
PORT = 8000

# 获取当前脚本所在目录作为网站根目录
web_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(web_dir)

# 创建请求处理器
Handler = http.server.SimpleHTTPRequestHandler

# 创建 TCP 服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"启动静态网站服务器在 http://localhost:{PORT}")
    print(f"网站根目录: {web_dir}")
    print("按 Ctrl+C 停止服务器")
    # 启动服务器，持续监听请求
    httpd.serve_forever()