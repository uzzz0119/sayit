"""
Flask应用工厂
"""
import os
from flask import Flask, g
from app.config import Config


def create_app(config_class=Config):
    """创建并配置Flask应用"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)
    
    # 确保所有必要的文件夹存在
    os.makedirs(app.config['VIDEOS_DIR'], exist_ok=True)
    os.makedirs(app.config['CAPTIONS_DIR'], exist_ok=True)
    os.makedirs(app.config['PDF_DIR'], exist_ok=True)
    os.makedirs(app.config['NOTES_DIR'], exist_ok=True)
    
    # 注册蓝图
    from app.routes import main_bp, notes_bp, generation_bp, learning_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
    app.register_blueprint(generation_bp, url_prefix='/api')
    app.register_blueprint(learning_bp, url_prefix='/api')
    
    # 注册请求后清理钩子
    @app.after_request
    def cleanup_files(response):
        """请求结束后，清理所有临时文件"""
        paths_to_clean = [
            g.get('audio_path'),
            g.get('caption_path'),
            g.get('pdf_path')
        ]
        for path in paths_to_clean:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"已清理临时文件: {path}")
                except OSError as e:
                    print(f"清理文件时出错: {e}")
        return response
    
    return app

