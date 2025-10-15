"""
影子跟读路由
处理视频列表和字幕segments数据
"""
import os
import json
from flask import Blueprint, jsonify, current_app, send_file

shadowing_bp = Blueprint('shadowing', __name__)


@shadowing_bp.route('/videos', methods=['GET'])
def get_videos():
    """
    获取所有可用的视频/音频列表
    返回格式：[{filename, title, has_segments, media_type}]
    """
    try:
        videos_dir = current_app.config['VIDEOS_DIR']
        captions_dir = current_app.config['CAPTIONS_DIR']
        
        if not os.path.exists(videos_dir):
            return jsonify([])
        
        videos = []
        for filename in os.listdir(videos_dir):
            if filename.endswith(('.mp4', '.mp3', '.webm', '.mkv', '.m4a', '.wav')):
                base_name = os.path.splitext(filename)[0]
                segments_path = os.path.join(captions_dir, f"{base_name}_segments.json")
                
                # 判断媒体类型
                ext = os.path.splitext(filename)[1].lower()
                media_type = 'audio' if ext in ['.mp3', '.m4a', '.wav'] else 'video'
                
                videos.append({
                    'filename': filename,
                    'title': base_name,
                    'has_segments': os.path.exists(segments_path),
                    'media_type': media_type
                })
        
        # 按修改时间倒序排列
        videos.sort(key=lambda x: os.path.getmtime(
            os.path.join(videos_dir, x['filename'])
        ), reverse=True)
        
        return jsonify(videos)
    
    except Exception as e:
        print(f"获取视频列表失败: {e}")
        return jsonify({"error": str(e)}), 500


@shadowing_bp.route('/videos/<filename>/segments', methods=['GET'])
def get_video_segments(filename):
    """
    获取视频的字幕segments
    """
    try:
        captions_dir = current_app.config['CAPTIONS_DIR']
        base_name = os.path.splitext(filename)[0]
        segments_path = os.path.join(captions_dir, f"{base_name}_segments.json")
        
        if not os.path.exists(segments_path):
            return jsonify({"error": "字幕文件不存在"}), 404
        
        with open(segments_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify(data)
    
    except Exception as e:
        print(f"获取字幕segments失败: {e}")
        return jsonify({"error": str(e)}), 500


@shadowing_bp.route('/videos/<filename>/stream', methods=['GET'])
def stream_video(filename):
    """
    流式传输视频/音频文件
    """
    try:
        videos_dir = current_app.config['VIDEOS_DIR']
        file_path = os.path.join(videos_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 根据文件扩展名确定mimetype
        ext = os.path.splitext(filename)[1].lower()
        mimetype_map = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mkv': 'video/x-matroska',
            '.mp3': 'audio/mpeg',
            '.m4a': 'audio/mp4',
            '.wav': 'audio/wav'
        }
        mimetype = mimetype_map.get(ext, 'application/octet-stream')
        
        return send_file(file_path, mimetype=mimetype)
    
    except Exception as e:
        print(f"流式传输文件失败: {e}")
        return jsonify({"error": str(e)}), 500

