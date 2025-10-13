"""
音频下载工具
使用yt-dlp下载并提取音频
"""
import os
import yt_dlp
from flask import current_app


def download_audio(video_url):
    """
    使用 yt-dlp 下载视频并提取为音频
    
    Args:
        video_url (str): 视频的 URL
    
    Returns:
        str: 下载的音频文件路径，如果失败则返回 None
    """
    try:
        videos_dir = current_app.config['VIDEOS_DIR']
        
        # 设置 yt-dlp 的选项
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(videos_dir, '%(id)s.%(ext)s'),
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_id = info_dict.get('id', None)
            audio_path = os.path.join(videos_dir, f"{video_id}.mp3")
            
            if os.path.exists(audio_path):
                print(f"音频下载成功: {audio_path}")
                return audio_path
            else:
                print("错误: 下载后未找到音频文件")
                return None

    except Exception as e:
        print(f"下载或转换音频时出错: {e}")
        return None

