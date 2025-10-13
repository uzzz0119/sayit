"""
字幕生成工具
使用Whisper模型进行语音识别
"""
import os
import whisper
from flask import current_app


def generate_caption(audio_path):
    """
    使用 Whisper 模型为给定的音频文件生成字幕
    
    Args:
        audio_path (str): 音频文件路径
    
    Returns:
        tuple: (caption_path, caption_text) 字幕文件路径和文本内容
    """
    try:
        print("正在加载 Whisper 模型...")
        model = whisper.load_model("base")
        print("模型加载完毕，开始生成字幕...")

        # 执行语音识别
        result = model.transcribe(audio_path, fp16=False)
        caption_text = result['text']

        # 从音频路径生成字幕文件的路径
        captions_dir = current_app.config['CAPTIONS_DIR']
        base_filename = os.path.basename(audio_path)
        filename_without_ext = os.path.splitext(base_filename)[0]
        caption_path = os.path.join(captions_dir, f"{filename_without_ext}.txt")

        # 将识别出的文本写入文件
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(caption_text)
        
        print(f"字幕生成成功: {caption_path}")
        return caption_path, caption_text

    except Exception as e:
        print(f"生成字幕时出错: {e}")
        return None, None

