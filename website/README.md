# Init K8s 静态官网

这是 Init K8s 项目的静态官网，使用 Python 内置的 HTTP 服务器提供服务。

## 如何运行

1. 确保您的系统已安装 Python 3
2. 进入当前目录
3. 运行以下命令启动服务器：

```bash
python3 app.py
```

4. 打开浏览器，访问 [http://localhost:8000](http://localhost:8000)

## 文件结构

- `app.py` - Python 服务器脚本
- `index.html` - 网站主页
- `styles.css` - 网站样式
- `script.js` - 交互脚本

## 功能特性

- 响应式设计，支持各种屏幕尺寸
- 平滑滚动导航
- 现代化的 UI 设计
- 简单易用的 Python 服务器

## 停止服务器

按 `Ctrl+C` 可以停止服务器。