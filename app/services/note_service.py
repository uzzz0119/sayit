"""
笔记管理服务
处理笔记的存储、检索、删除等操作
"""
import os
import json
from datetime import datetime
from flask import current_app


class NoteService:
    """笔记服务类"""
    
    @staticmethod
    def _get_index_file():
        """获取索引文件路径"""
        return current_app.config['NOTES_INDEX_FILE']
    
    @staticmethod
    def _get_notes_dir():
        """获取笔记目录路径"""
        return current_app.config['NOTES_DIR']
    
    @staticmethod
    def load_index():
        """加载笔记索引"""
        index_file = NoteService._get_index_file()
        if os.path.exists(index_file):
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    @staticmethod
    def save_index(notes_list):
        """保存笔记索引"""
        index_file = NoteService._get_index_file()
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(notes_list, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def add_to_index(filename, title, note_type, template_ref=None):
        """添加笔记到索引
        
        Args:
            filename: 文件名
            title: 标题
            note_type: 类型 ('video', 'music', 'article', 'learning')
            template_ref: 模板引用（用于学习笔记）
        """
        notes = NoteService.load_index()
        note_entry = {
            'filename': filename,
            'title': title,
            'type': note_type,
            'created_at': datetime.now().isoformat()
        }
        
        # 如果有模板引用，添加到记录中
        if template_ref:
            note_entry['template_ref'] = template_ref
        
        notes.insert(0, note_entry)  # 插入到最前面
        NoteService.save_index(notes)
    
    @staticmethod
    def remove_from_index(filename):
        """从索引中移除笔记"""
        notes = NoteService.load_index()
        notes = [n for n in notes if n['filename'] != filename]
        NoteService.save_index(notes)
    
    @staticmethod
    def get_all_notes():
        """获取所有笔记列表"""
        return NoteService.load_index()
    
    @staticmethod
    def get_note_path(filename):
        """获取笔记文件路径"""
        notes_dir = NoteService._get_notes_dir()
        note_path = os.path.join(notes_dir, filename)
        if os.path.exists(note_path):
            return note_path
        return None
    
    @staticmethod
    def get_note_content(filename):
        """获取笔记内容"""
        note_path = NoteService.get_note_path(filename)
        if note_path is None:
            return None
        
        try:
            with open(note_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return None
    
    @staticmethod
    def save_note(filename, content, title, note_type, template_ref=None):
        """保存笔记
        
        Args:
            filename: 文件名
            content: 笔记内容
            title: 标题
            note_type: 类型
            template_ref: 模板引用（可选）
        """
        notes_dir = NoteService._get_notes_dir()
        note_path = os.path.join(notes_dir, filename)
        
        try:
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 添加到索引
            NoteService.add_to_index(filename, title, note_type, template_ref)
            print(f"笔记已保存: {note_path}")
            return True
        except Exception as e:
            print(f"保存笔记失败: {e}")
            return False
    
    @staticmethod
    def save_learning_note(chinese_text, english_text, template_filename=None, template_title=None):
        """保存学习笔记
        
        Args:
            chinese_text: 中文原文
            english_text: 英文翻译
            template_filename: 模板文件名（可选）
            template_title: 模板标题（可选）
        
        Returns:
            dict: 包含 filename 和 title 的字典，失败返回 None
        """
        from hashlib import md5
        from datetime import datetime
        
        # 生成唯一文件名（使用时间戳和内容哈希）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        content_hash = md5(chinese_text.encode()).hexdigest()[:8]
        filename = f"learning_{timestamp}_{content_hash}.md"
        
        # 生成笔记标题（使用中文前20个字符）
        title = chinese_text[:20] + ('...' if len(chinese_text) > 20 else '')
        
        # 构建笔记内容
        content_parts = [
            "# 强化学习笔记\n",
            f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        ]
        
        if template_filename and template_title:
            content_parts.append(f"**参考模板**: {template_title}\n")
        
        content_parts.extend([
            "\n---\n\n",
            "## 中文原文\n\n",
            f"{chinese_text}\n\n",
            "---\n\n",
            "## 英文翻译\n\n",
            f"{english_text}\n"
        ])
        
        content = "".join(content_parts)
        
        # 保存笔记
        template_ref = template_filename if template_filename else None
        success = NoteService.save_note(filename, content, title, 'learning', template_ref)
        
        if success:
            return {
                'filename': filename,
                'title': title
            }
        return None
    
    @staticmethod
    def delete_note(filename):
        """删除笔记"""
        note_path = NoteService.get_note_path(filename)
        
        try:
            # 删除文件
            if note_path and os.path.exists(note_path):
                os.remove(note_path)
            
            # 从索引移除
            NoteService.remove_from_index(filename)
            return True
        except Exception as e:
            print(f"删除笔记失败: {e}")
            return False

