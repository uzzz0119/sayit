"""
音频/视频下载工具
使用yt-dlp下载视频或提取音频
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


def download_video(video_url, download_type='video'):
    """
    使用 yt-dlp 下载视频（含音频和画面）
    
    Args:
        video_url (str): 视频的 URL
        download_type (str): 下载类型，'video' 表示下载视频
    
    Returns:
        str: 下载的视频文件路径，如果失败则返回 None
    """
    import time
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            videos_dir = current_app.config['VIDEOS_DIR']
            
            # 设置 yt-dlp 的选项 - 下载最佳视频+音频
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(videos_dir, '%(id)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'merge_output_format': 'mp4',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_id = info_dict.get('id', None)
                video_path = os.path.join(videos_dir, f"{video_id}.mp4")
                
                if os.path.exists(video_path):
                    print(f"视频下载成功: {video_path}")
                    return video_path
                else:
                    print("错误: 下载后未找到视频文件")
                    return None

        except Exception as e:
            print(f"下载视频时出错 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print("等待 3 秒后重试...")
                time.sleep(3)
            else:
                print("视频下载失败，已达最大重试次数")
                return None
    
    return None
