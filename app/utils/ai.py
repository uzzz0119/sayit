"""
AI工具
使用OpenAI API进行文本生成、转换和语音合成
"""
import os
from openai import OpenAI


def generate_notes_from_text(caption_text):
    """
    使用 OpenAI API 将字幕文本转换为结构化笔记
    
    Args:
        caption_text (str): 字幕文本
    
    Returns:
        str: 生成的笔记文本
    """
    try:
        print("正在调用大语言模型生成笔记...")
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        if not api_key:
            print("错误: 未设置 OPENAI_API_KEY 环境变量。")
            return None
        
        client = OpenAI(api_key=api_key, base_url=base_url)

        prompt = f"""
你是一个专业的英语学习笔记整理助手。
你的任务是将用户提供的视频字幕文本，逐句转换成结构化的学习笔记。

重要提示：请确保对字幕中的【每一句话】都生成笔记，不要遗漏任何句子。即使某些句子看似简单，也要提供学习笔记。

请严格按照以下要求输出，不要添加任何额外解释、开场白或总结：

输出格式
对于字幕中的每一句话，生成一个独立的笔记条目，格式如下：

序号. 英文句子
短语/句式：提取并讲解 1-2 个常用短语或句式
中文：对整个句子的地道中文翻译
应用：基于该句子的语法或短语，创造 1-2 个日常生活中的英文例句
补充说明：如果有语法点、文化背景或使用场景，请简要说明

规则说明

英文句子：完整保留原句，不做修改。

短语/句式：必须是该句子中有学习价值的表达，并给出简洁解释（如 "count the days until ... = 迫不及待地等到……"）。

中文翻译：提供自然、流畅的中文翻译，不要逐词硬译。

应用例句：根据提取的短语或句式，创造 1-2 个与日常生活相关的英文例句。

补充说明：提供额外的学习价值，如语法解析、使用场景等。

字幕文本：
"{caption_text}"

请现在开始生成详细的笔记，确保每个句子都有对应的条目：
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的英语学习笔记整理助手。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        notes_text = response.choices[0].message.content
        print("笔记生成成功。")
        return notes_text.strip()

    except Exception as e:
        print(f"调用大语言模型时出错: {e}")
        return None


def generate_lyrics_notes_from_text(lyrics_text, song_name="", artist_name=""):
    """
    使用 OpenAI API 将歌词文本转换为学习笔记
    
    Args:
        lyrics_text (str): 歌词文本
        song_name (str): 歌曲名
        artist_name (str): 歌手名
    
    Returns:
        str: 生成的笔记文本
    """
    try:
        print("正在调用大语言模型生成歌词笔记...")
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        if not api_key:
            print("错误: 未设置 OPENAI_API_KEY 环境变量。")
            return None
        
        client = OpenAI(api_key=api_key, base_url=base_url)

        title_section = f"歌曲：{song_name}\n歌手：{artist_name}\n\n" if song_name else ""

        prompt = f"""
你是一个专业的英语学习笔记整理助手。
你的任务是将英文歌词转换成结构化的学习笔记。

{title_section}请严格按照以下要求输出，不要添加任何额外解释、开场白或总结：

输出格式
对于歌词中的每一句有意义的歌词（跳过重复的副歌可以只分析一次），生成一个独立的笔记条目，格式如下：

序号. 英文歌词
短语/句式：提取并讲解 1-2 个常用短语、俚语或句式
中文：对整句歌词的地道中文翻译（考虑歌词意境）
应用：基于该句的短语或表达，创造 1-2 个日常生活中的英文例句
补充说明：如果有语法点、文化背景、隐喻含义或使用场景，请简要说明

规则说明

1. 英文歌词：完整保留原句
2. 短语/句式：必须是该句中有学习价值的表达
3. 中文翻译：提供自然、流畅、符合歌词意境的中文翻译
4. 应用例句：根据提取的短语创造实用的日常例句
5. 补充说明：提供额外的学习价值，如俚语解释、文化背景等
6. 对于重复出现的副歌部分，只需分析一次

歌词内容：
"{lyrics_text}"

请现在开始生成详细的笔记：
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个专业的英语歌词学习笔记整理助手。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        notes_text = response.choices[0].message.content
        
        # 在笔记前添加歌曲信息
        full_notes = f"{'='*50}\n{title_section}{'='*50}\n\n{notes_text}"
        
        print("歌词笔记生成成功。")
        return full_notes.strip()

    except Exception as e:
        print(f"调用大语言模型时出错: {e}")
        return None


def transform_chinese_to_english(chinese_text, note_content=None, has_note=False):
    """
    将中文文本转换为地道的美式英语
    
    Args:
        chinese_text (str): 中文文本
        note_content (str): 笔记内容（可选，作为模板）
        has_note (bool): 是否使用笔记作为模板
    
    Returns:
        str: 转换后的英文文本
    """
    try:
        print("正在调用大语言模型进行文本转换...")
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        if not api_key:
            error_msg = "未设置 OPENAI_API_KEY 环境变量。请创建 .env 文件并添加API密钥。"
            print(f"错误: {error_msg}")
            raise ValueError(error_msg)
        
        client = OpenAI(api_key=api_key, base_url=base_url)

        if has_note and note_content:
            # 使用笔记作为模板
            prompt = f"""
你是一位专业的英语 vlog 表达教练和脚本创作助手。

你的任务：
将用户的中文内容转化为一段地道、自然、有情绪节奏的 美式英语 vlog 独白（vlogger monologue）。

写作要求：

1. 不逐字翻译，要重构语序，像 vlog 主人自然讲述一样。

2. 模仿笔记模板的语气、句式与词汇风格，但内容要完全围绕用户的中文表达。

3. 英语应简洁流畅，句式自然，平均每句不超过20词。

4. 使用 短语动词（phrasal verbs）、生活化表达（everyday English），并带有轻松随意的 纽约口语腔调。

5. 保持完整叙事感：从"动作 → 感受 → 结果"三层结构组织语言。


模板参考：

{note_content[:2000]}

用户输入：

{chinese_text}

输出格式：

请直接输出一段自然的 vlog 风格英文独白，用 ** 标记来自模板的短语或表达。
"""
        else:
            # 不使用笔记模板
            prompt = f"""
你是一个专业的英语表达助手。

任务：将用户的中文内容转换为地道的美式英语。

重要要求：
1. 不需要逐字翻译，但尽量保留细节
2. 请分析清楚用户的内容，而后用英文重新逻辑清晰地组织它
3. 使用地道的美式英语，纽约腔调
4. 尽量使用日常词汇
5. 优先使用短语动词或者习惯用语（phrasal verbs and idioms）
6. 每个句子最长不超过20个单词
7. 保持自然、口语化的表达

用户的中文内容：
{chinese_text}

请直接输出转换后的英文，不要添加任何解释或说明：
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个专业的英语表达助手，擅长将中文转换为地道的美式英语。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        english_text = response.choices[0].message.content.strip()
        
        if not english_text:
            raise ValueError("API返回了空响应")
        
        print("文本转换成功。")
        return english_text

    except ValueError as e:
        # 配置错误，直接抛出
        print(f"配置错误: {e}")
        raise
    except Exception as e:
        # API调用错误，提供详细信息
        error_msg = f"API调用失败: {str(e)}"
        print(f"调用大语言模型时出错: {error_msg}")
        raise Exception(error_msg)


def text_to_speech(text):
    """
    将英文文本转换为语音（女声）
    使用 OpenAI TTS API
    
    Args:
        text (str): 英文文本
    
    Returns:
        bytes: 音频内容（MP3格式）
    
    Raises:
        ValueError: 配置错误
        Exception: API 调用失败
    """
    try:
        print("正在生成语音...")
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        if not api_key:
            error_msg = "未设置 OPENAI_API_KEY 环境变量"
            print(f"错误: {error_msg}")
            raise ValueError(error_msg)
        
        if not text or not text.strip():
            error_msg = "文本内容为空"
            print(f"错误: {error_msg}")
            raise ValueError(error_msg)
        
        client = OpenAI(api_key=api_key, base_url=base_url)

        # 使用 OpenAI TTS API
        # voice options: alloy, echo, fable, onyx, nova, shimmer
        # nova 是女声，比较自然
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # 女声
            input=text.strip(),
            speed=1.0
        )
        
        # 返回音频内容
        audio_content = response.content
        
        if not audio_content:
            raise ValueError("API 返回了空的音频内容")
        
        print(f"语音生成成功，大小: {len(audio_content)} 字节")
        return audio_content

    except ValueError as e:
        # 配置错误或参数错误
        print(f"TTS 配置错误: {e}")
        raise
    except Exception as e:
        # API 调用错误
        error_msg = f"TTS API 调用失败: {str(e)}"
        print(f"生成语音时出错: {error_msg}")
        raise Exception(error_msg)

