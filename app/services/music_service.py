"""
音乐处理服务
处理QQ音乐歌词提取和笔记生成
"""
import os
from flask import current_app
from app.utils.music import extract_qq_music_song_id, get_qq_music_lyrics
from app.utils.ai import generate_lyrics_notes_from_text
from app.utils.pdf import create_pdf_from_notes
from app.services.note_service import NoteService


class MusicService:
    """音乐处理服务类"""
    
    @staticmethod
    def process_qq_music(music_url, output_format='pdf', save_to_storage=False):
        """
        处理QQ音乐链接，提取歌词并生成笔记
        
        Args:
            music_url: QQ音乐URL
            output_format: 输出格式 ('txt' 或 'pdf')
            save_to_storage: 是否保存到笔记存储区
        
        Returns:
            dict: 处理结果
        """
        result = {'status': 'success'}
        
        # 1. 提取歌曲ID
        song_id = extract_qq_music_song_id(music_url)
        if not song_id:
            return {'status': 'error', 'message': '无法从链接中提取歌曲ID，请检查链接格式'}
        
        # 2. 获取歌词
        song_name, artist_name, lyrics_text = get_qq_music_lyrics(song_id)
        if not lyrics_text:
            return {'status': 'error', 'message': '无法获取该歌曲的歌词'}
        
        result['song_name'] = song_name
        result['artist_name'] = artist_name
        
        # 3. 根据输出格式处理
        if output_format == 'txt':
            lyrics_with_info = f"歌曲：{song_name}\n歌手：{artist_name}\n{'='*50}\n\n{lyrics_text}"
            result['lyrics_text'] = lyrics_with_info
            result['filename'] = f"{song_name}_lyrics.txt"
            return result
        
        # 4. 生成PDF笔记
        notes_text = generate_lyrics_notes_from_text(lyrics_text, song_name, artist_name)
        if not notes_text:
            return {'status': 'error', 'message': '调用大模型生成歌词笔记失败'}
        
        # 5. 保存MD格式笔记到存储区
        if save_to_storage:
            md_filename = f"{song_id}_lyrics_notes.md"
            music_title = f"{song_name} - {artist_name}"
            NoteService.save_note(md_filename, notes_text, music_title, 'music')
        
        # 6. 创建PDF文件
        pdf_filename = f"{song_id}_lyrics_notes.pdf"
        pdf_dir = current_app.config['PDF_DIR']
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        created_pdf_path = create_pdf_from_notes(notes_text, pdf_path)
        if not created_pdf_path:
            return {'status': 'error', 'message': '创建 PDF 文件失败'}
        
        result['pdf_path'] = created_pdf_path
        result['filename'] = f"{song_name}_歌词笔记.pdf"
        
        return result

