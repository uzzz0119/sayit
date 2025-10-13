"""
路由蓝图
"""
from app.routes.main import main_bp
from app.routes.notes import notes_bp
from app.routes.generation import generation_bp
from app.routes.learning import learning_bp

__all__ = ['main_bp', 'notes_bp', 'generation_bp', 'learning_bp']

