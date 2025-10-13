"""
视频处理服务
处理视频下载、字幕提取、笔记生成
"""
import os
from flask import current_app
from app.utils.audio import download_audio
from app.utils.caption import generate_caption
from app.utils.ai import generate_notes_from_text
from app.utils.pdf import create_pdf_from_notes
from app.services.note_service import NoteService


class VideoService:
    """视频处理服务类"""
    
    @staticmethod
    def process_video(video_url, output_format='pdf', save_to_storage=False):
        """
        处理视频，生成字幕和笔记
        
        Args:
            video_url: 视频URL
            output_format: 输出格式 ('txt' 或 'pdf')
            save_to_storage: 是否保存到笔记存储区
        
        Returns:
            dict: 处理结果
        """
        result = {'status': 'success'}
        
        # 1. 下载和提取音频
        audio_path = download_audio(video_url)
        if not audio_path:
            return {'status': 'error', 'message': '无法下载或处理该视频链接'}
        result['audio_path'] = audio_path
        
        # 2. 生成字幕文本
        caption_path, caption_text = generate_caption(audio_path)
        if not caption_path:
            return {'status': 'error', 'message': '生成字幕失败'}
        result['caption_path'] = caption_path
        result['caption_text'] = caption_text
        
        # 3. 根据输出格式处理
        if output_format == 'txt':
            result['filename'] = os.path.basename(caption_path)
            return result
        
        # 4. 生成PDF笔记
        notes_text = generate_notes_from_text(caption_text)
        if not notes_text:
            return {'status': 'error', 'message': '调用大模型生成笔记失败'}
        
        # 5. 保存MD格式笔记到存储区
        if save_to_storage:
            base_filename = os.path.splitext(os.path.basename(caption_path))[0]
            md_filename = f"{base_filename}_notes.md"
            video_title = f"视频笔记_{base_filename[:20]}"
            NoteService.save_note(md_filename, notes_text, video_title, 'video')
        
        # 6. 创建PDF文件
        base_filename = os.path.splitext(os.path.basename(caption_path))[0]
        pdf_filename = f"{base_filename}_notes.pdf"
        pdf_dir = current_app.config['PDF_DIR']
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        created_pdf_path = create_pdf_from_notes(notes_text, pdf_path)
        if not created_pdf_path:
            return {'status': 'error', 'message': '创建 PDF 文件失败'}
        
        result['pdf_path'] = created_pdf_path
        result['filename'] = pdf_filename
        
        return result

