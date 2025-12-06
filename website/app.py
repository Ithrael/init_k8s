import http.server
import socketserver
import os
import sys

# 设置默认端口
DEFAULT_PORT = 80

# 获取当前脚本所在目录作为网站根目录
web_dir = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加缓存策略
        if self.path.endswith('.html') or self.path.endswith('/'):
            # HTML文件缓存1小时
            self.send_header('Cache-Control', 'public, max-age=3600')
        elif self.path.endswith(('.css', '.js', '.png', '.jpg', '.svg')):
            # 静态资源缓存1天
            self.send_header('Cache-Control', 'public, max-age=86400')
        else:
            self.send_header('Cache-Control', 'no-cache')
        
        super().end_headers()

def main(port=DEFAULT_PORT):
    os.chdir(web_dir)
    # 创建请求处理器
    Handler = CustomHandler

    # 创建 TCP 服务器
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"启动静态网站服务器在 http://localhost:{port}")
            print(f"网站根目录: {web_dir}")
            print("按 Ctrl+C 停止服务器")
            # 启动服务器，持续监听请求
            httpd.serve_forever()
    except PermissionError:
        print(f"错误: 无法绑定到端口 {port}。可能需要管理员权限 (sudo)。")
        sys.exit(1)
    except OSError as e:
        print(f"启动服务器失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 允许通过命令行参数指定端口
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("端口必须是整数")
            sys.exit(1)
    main(port)