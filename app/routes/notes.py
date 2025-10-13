"""
笔记管理路由
处理笔记的CRUD操作
"""
from flask import Blueprint, jsonify, send_file, current_app
from app.services.note_service import NoteService

notes_bp = Blueprint('notes', __name__)


@notes_bp.route('', methods=['GET'])
def get_notes_list():
    """获取笔记列表"""
    try:
        notes = NoteService.get_all_notes()
        return jsonify(notes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notes_bp.route('/<filename>', methods=['GET'])
def get_note_content(filename):
    """获取单个笔记内容"""
    try:
        content = NoteService.get_note_content(filename)
        if content is None:
            return jsonify({"error": "笔记不存在"}), 404
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notes_bp.route('/<filename>/download', methods=['GET'])
def download_note(filename):
    """下载笔记"""
    try:
        note_path = NoteService.get_note_path(filename)
        if note_path is None:
            return jsonify({"error": "笔记不存在"}), 404
        return send_file(note_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notes_bp.route('/<filename>', methods=['DELETE'])
def delete_note(filename):
    """删除笔记"""
    try:
        success = NoteService.delete_note(filename)
        if not success:
            return jsonify({"error": "删除失败"}), 500
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

