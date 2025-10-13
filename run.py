"""
应用入口文件
"""
import os
from dotenv import load_dotenv
from app import create_app

# 加载环境变量
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

