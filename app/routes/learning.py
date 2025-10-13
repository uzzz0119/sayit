"""
强化学习路由
处理文本转换和学习笔记保存
"""
from flask import Blueprint, request, jsonify
from app.services.ai_service import AIService
from app.services.note_service import NoteService

learning_bp = Blueprint('learning', __name__)


@learning_bp.route('/transform-text', methods=['POST'])
def transform_text():
    """
    将中文文本转换为地道的美式英语
    接受参数：
    - chinese_text: 中文文本
    - note_content: 笔记内容（可选，作为模板）
    - has_note: 是否使用笔记作为模板
    """
    data = request.get_json()
    if not data or 'chinese_text' not in data:
        return jsonify({"error": "请求体中缺少 'chinese_text'"}), 400

    chinese_text = data['chinese_text']
    note_content = data.get('note_content')
    has_note = data.get('has_note', False)

    print(f"接收到文本转换请求，中文长度: {len(chinese_text)}, 是否使用笔记模板: {has_note}")

    try:
        english_text = AIService.transform_chinese_to_english(
            chinese_text=chinese_text,
            note_content=note_content,
            has_note=has_note
        )
        
        return jsonify({
            "status": "success",
            "english_text": english_text
        })
    except ValueError as e:
        # 配置错误（如API密钥未设置）
        print(f"配置错误: {e}")
        return jsonify({"error": f"配置错误: {str(e)}"}), 500
    except Exception as e:
        # 其他错误（如API调用失败）
        print(f"文本转换出错: {e}")
        return jsonify({"error": f"{str(e)}"}), 500


@learning_bp.route('/save-note', methods=['POST'])
def save_learning_note():
    """
    保存学习笔记
    接受参数：
    - chinese_text: 中文原文
    - english_text: 英文翻译
    - template_filename: 模板文件名（可选）
    - template_title: 模板标题（可选）
    """
    data = request.get_json()
    
    if not data or 'chinese_text' not in data or 'english_text' not in data:
        return jsonify({"error": "请求体中缺少必要参数"}), 400
    
    chinese_text = data['chinese_text']
    english_text = data['english_text']
    template_filename = data.get('template_filename')
    template_title = data.get('template_title')
    
    print(f"接收到保存笔记请求，中文长度: {len(chinese_text)}")
    
    try:
        result = NoteService.save_learning_note(
            chinese_text=chinese_text,
            english_text=english_text,
            template_filename=template_filename,
            template_title=template_title
        )
        
        if not result:
            return jsonify({"error": "保存笔记失败"}), 500
        
        return jsonify({
            "status": "success",
            "filename": result['filename'],
            "title": result['title']
        })
    except Exception as e:
        print(f"保存笔记出错: {e}")
        return jsonify({"error": f"保存笔记时出错: {str(e)}"}), 500



