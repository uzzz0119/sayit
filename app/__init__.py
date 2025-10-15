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
    from app.routes.shadowing import shadowing_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
    app.register_blueprint(generation_bp, url_prefix='/api')
    app.register_blueprint(learning_bp, url_prefix='/api')
    app.register_blueprint(shadowing_bp, url_prefix='/api/shadowing')
    
    # 注册请求后清理钩子
    @app.after_request
    def cleanup_files(response):
        """
        请求结束后，清理临时文件
        注意：不清理videos和captions文件夹中的文件（用于影子跟读）
        """
        # 只清理标记为临时的PDF文件
        # 音频、视频、字幕文件需要保留用于影子跟读
        temp_pdf = g.get('temp_pdf_path')
        if temp_pdf and os.path.exists(temp_pdf):
            try:
                os.remove(temp_pdf)
                print(f"Cleaned temporary PDF: {temp_pdf}")
            except OSError as e:
                print(f"Error cleaning temp file: {e}")
        
        # 注意：不再清理audio_path, caption_path等
        # 这些文件需要保留用于影子跟读功能
        return response
    
    return app

