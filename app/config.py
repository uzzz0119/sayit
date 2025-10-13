"""
应用配置文件
"""
import os


class Config:
    """基础配置类"""
    
    # 基础目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 数据目录
    VIDEOS_DIR = os.path.join(BASE_DIR, 'videos')
    CAPTIONS_DIR = os.path.join(BASE_DIR, 'captions')
    PDF_DIR = os.path.join(BASE_DIR, 'pdfs')
    NOTES_DIR = os.path.join(BASE_DIR, 'notes')
    
    # 索引文件
    NOTES_INDEX_FILE = os.path.join(BASE_DIR, 'notes_index.json')
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # API配置
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

