"""
笔记生成路由
处理视频字幕、音乐歌词等内容的笔记生成
"""
from flask import Blueprint, request, jsonify, g, send_file, current_app
from app.services.video_service import VideoService
from app.services.music_service import MusicService

generation_bp = Blueprint('generation', __name__)


@generation_bp.route('/caption', methods=['POST'])
def generate_video_caption():
    """
    生成视频字幕笔记
    接受参数：
    - video_url: 视频链接
    - output_format: 'txt' 或 'pdf'，默认为 'pdf'
    - save_to_storage: 是否保存到笔记存储区
    """
    data = request.get_json()
    if not data or 'video_url' not in data:
        return jsonify({"error": "请求体中缺少 'video_url'"}), 400

    video_url = data['video_url']
    output_format = data.get('output_format', 'txt').lower()
    save_to_storage = data.get('save_to_storage', False)

    if output_format not in ['txt', 'pdf']:
        return jsonify({"error": "无效的 'output_format' 参数，只接受 'txt' 或 'pdf'"}), 400

    print(f"接收到视频链接: {video_url}, 输出格式: {output_format}")

    try:
        result = VideoService.process_video(
            video_url=video_url,
            output_format=output_format,
            save_to_storage=save_to_storage
        )
        
        if result['status'] == 'error':
            return jsonify({"error": result['message']}), 500
        
        # 记录临时文件路径，用于清理
        if 'audio_path' in result:
            g.audio_path = result['audio_path']
        if 'caption_path' in result:
            g.caption_path = result['caption_path']
        if 'pdf_path' in result:
            g.pdf_path = result['pdf_path']
        
        # 返回文本或PDF
        if output_format == 'txt':
            return jsonify({
                "status": "success",
                "caption": result['caption_text'],
                "filename": result['filename']
            })
        else:  # pdf
            return send_file(
                result['pdf_path'],
                as_attachment=True,
                download_name=result['filename']
            )
    
    except Exception as e:
        print(f"处理视频时出错: {e}")
        return jsonify({"error": f"处理视频时出错: {str(e)}"}), 500


@generation_bp.route('/qq-music-lyrics', methods=['POST'])
def generate_music_lyrics():
    """
    生成QQ音乐歌词笔记
    接受参数：
    - music_url: QQ音乐链接
    - output_format: 'txt' 或 'pdf'，默认为 'pdf'
    - save_to_storage: 是否保存到笔记存储区
    """
    data = request.get_json()
    if not data or 'music_url' not in data:
        return jsonify({"error": "请求体中缺少 'music_url'"}), 400

    music_url = data['music_url']
    output_format = data.get('output_format', 'pdf').lower()
    save_to_storage = data.get('save_to_storage', False)

    if output_format not in ['txt', 'pdf']:
        return jsonify({"error": "无效的 'output_format' 参数，只接受 'txt' 或 'pdf'"}), 400

    print(f"接收到QQ音乐链接: {music_url}, 输出格式: {output_format}")

    try:
        result = MusicService.process_qq_music(
            music_url=music_url,
            output_format=output_format,
            save_to_storage=save_to_storage
        )
        
        if result['status'] == 'error':
            return jsonify({"error": result['message']}), 500
        
        # 记录PDF路径用于清理
        if 'pdf_path' in result:
            g.pdf_path = result['pdf_path']
        
        # 返回文本或PDF
        if output_format == 'txt':
            return jsonify({
                "status": "success",
                "song_name": result['song_name'],
                "artist_name": result['artist_name'],
                "lyrics": result['lyrics_text'],
                "filename": result['filename']
            })
        else:  # pdf
            return send_file(
                result['pdf_path'],
                as_attachment=True,
                download_name=result['filename']
            )
    
    except Exception as e:
        print(f"处理QQ音乐时出错: {e}")
        return jsonify({"error": f"处理QQ音乐时出错: {str(e)}"}), 500

