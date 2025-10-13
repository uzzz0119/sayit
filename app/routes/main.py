"""
主页路由
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """渲染首页（Figma 设计页面）"""
    return render_template('index.html')


@main_bp.route('/app')
def app():
    """渲染应用页面"""
    return render_template('app.html')

