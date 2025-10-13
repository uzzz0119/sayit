"""
PDF生成工具
使用ReportLab生成PDF文件
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT


def create_pdf_from_notes(notes_text, pdf_path):
    """
    使用 reportlab 将格式化的笔记文本生成 PDF 文件
    支持中文和自动换行
    
    Args:
        notes_text (str): 笔记文本
        pdf_path (str): PDF文件保存路径
    
    Returns:
        str: 创建的PDF文件路径，失败返回None
    """
    try:
        print(f"正在创建 PDF 文件: {pdf_path}")
        
        # 字体注册
        font_path = "C:/Windows/Fonts/simsun.ttc"  # 宋体
        if not os.path.exists(font_path):
            font_path = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
            if not os.path.exists(font_path):
                print("警告：找不到中文字体文件，PDF 中文可能无法显示。")
                registered_font_name = "Helvetica"  # 后备字体
            else:
                registered_font_name = 'ChineseFont'
                pdfmetrics.registerFont(TTFont(registered_font_name, font_path))
        else:
            registered_font_name = 'ChineseFont'
            pdfmetrics.registerFont(TTFont(registered_font_name, font_path))

        # 创建样式表
        styles = getSampleStyleSheet()
        note_style = ParagraphStyle(
            'NoteStyle',
            parent=styles['Normal'],
            fontName=registered_font_name,
            fontSize=10,
            leading=14,  # 行间距
            alignment=TA_LEFT,  # 左对齐
        )

        # 绘制 PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # 定义内容区域的边距和宽度
        margin = 50
        content_width = width - 2 * margin
        
        y = height - margin  # 设置起始 y 坐标
        
        # 将整个笔记文本分割成独立的行
        lines = notes_text.split('\n')
        
        for line in lines:
            # 将每一行文本包装成一个 Paragraph 对象
            p = Paragraph(line, note_style)
            
            # wrapOn 方法计算段落需要的高度和宽度
            p_width, p_height = p.wrapOn(c, content_width, height)
            
            # 如果当前段落会超出页面底部，则新建一页
            if y - p_height < margin:
                c.showPage()
                y = height - margin  # 重置 y 坐标到新页面的顶部
            
            # 在计算好的位置绘制段落
            p.drawOn(c, margin, y - p_height)
            
            # 更新 y 坐标
            y -= p_height

        c.save()
        print("PDF 文件创建成功。")
        return pdf_path
        
    except Exception as e:
        print(f"创建 PDF 时出错: {e}")
        return None

