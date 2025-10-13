"""
业务服务层
"""
from app.services.note_service import NoteService
from app.services.video_service import VideoService
from app.services.music_service import MusicService
from app.services.ai_service import AIService

__all__ = ['NoteService', 'VideoService', 'MusicService', 'AIService']

