"""
AI服务
处理文本转换
"""
from app.utils.ai import transform_chinese_to_english


class AIService:
    """AI服务类"""
    
    @staticmethod
    def transform_chinese_to_english(chinese_text, note_content=None, has_note=False):
        """
        将中文文本转换为地道的美式英语
        
        Args:
            chinese_text: 中文文本
            note_content: 笔记内容（作为模板）
            has_note: 是否使用笔记作为模板
        
        Returns:
            str: 英文文本
        """
        return transform_chinese_to_english(chinese_text, note_content, has_note)

