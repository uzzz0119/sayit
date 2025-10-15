"""
字幕生成工具
使用 Faster-Whisper 进行语音识别（支持词级时间戳）
"""
import os
import json
import re
from faster_whisper import WhisperModel
from app.utils.ai import get_sentence_break_indices_by_llm, restore_sentence_final_punct_by_llm
from flask import current_app


def split_by_sentence(text, start_time, end_time, words=None):
    """
    严格按句子结束符（. ! ?）分割文本，保留标点符号
    
    Args:
        text: 文本内容
        start_time: 开始时间
        end_time: 结束时间
        words: 单词级别的时间戳数据（未使用）
    
    Returns:
        list: 分割后的句子列表，每个包含 start, end, text
    """
    text = text.strip()
    
    # 查找所有句子结束符的位置（. ! ?）
    sentences = []
    current_start = 0
    
    for i, char in enumerate(text):
        if char in '.!?':
            # 找到句子结束符，提取从current_start到i+1（包含标点）
            sentence = text[current_start:i+1].strip()
            if sentence:
                sentences.append(sentence)
            current_start = i + 1
    
    # 处理最后一部分（如果没有结束符）
    if current_start < len(text):
        remaining = text[current_start:].strip()
        if remaining:
            sentences.append(remaining)
    
    # 如果没有找到句子，返回原文
    if not sentences:
        return [{
            'start': start_time,
            'end': end_time,
            'text': text
        }]
    
    # 如果只有一个句子，直接返回
    if len(sentences) == 1:
        return [{
            'start': start_time,
            'end': end_time,
            'text': sentences[0]
        }]
    
    # 计算每个句子的时间（按字符比例分配）
    total_duration = end_time - start_time
    total_chars = sum(len(s) for s in sentences)
    
    result = []
    current_time = start_time
    
    for i, sentence in enumerate(sentences):
        # 根据字符数比例分配时间
        sentence_duration = (len(sentence) / total_chars) * total_duration
        sentence_end = current_time + sentence_duration
        
        # 确保最后一句的结束时间准确
        if i == len(sentences) - 1:
            sentence_end = end_time
        
        result.append({
            'start': round(current_time, 2),
            'end': round(sentence_end, 2),
            'text': sentence
        })
        
        current_time = sentence_end
    
    return result


def split_by_length(text, start_time, end_time, max_length=80):
    """
    按固定长度分割（当没有句子边界时）
    """
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    # 分配时间
    total_duration = end_time - start_time
    total_chars = len(text)
    
    result = []
    current_time = start_time
    
    for i, chunk in enumerate(chunks):
        chunk_duration = (len(chunk) / total_chars) * total_duration
        chunk_end = current_time + chunk_duration
        
        if i == len(chunks) - 1:
            chunk_end = end_time
        
        result.append({
            'start': round(current_time, 2),
            'end': round(chunk_end, 2),
            'text': chunk.strip()
        })
        
        current_time = chunk_end
    
    return result


def split_long_segment(segment_text, start_time, end_time, max_duration=8.0):
    """
    分割过长的segment（超过max_duration秒）
    使用更智能的断句策略：
    1. 优先按句子标点（. ! ?）分割
    2. 次选按逗号（,）或分号（;）分割
    3. 最后按固定单词数量分割
    """
    duration = end_time - start_time
    if duration <= max_duration:
        return [{
            'start': start_time,
            'end': end_time,
            'text': segment_text
        }]
    
    sentences = []
    
    # 第一步：按句子结束标点分割（. ! ?）
    sentence_pattern = r'(?<=[.!?])\s+'
    potential_sentences = re.split(sentence_pattern, segment_text)
    
    for sent in potential_sentences:
        sent = sent.strip()
        if not sent:
            continue
        
        # 如果单个句子仍然太长（估算超过5秒），按逗号分割
        estimated_duration = (len(sent) / len(segment_text)) * duration
        if estimated_duration > 5.0 and ',' in sent:
            # 按逗号分割
            comma_parts = sent.split(',')
            current_part = ""
            for part in comma_parts:
                if current_part:
                    test_part = current_part + ',' + part
                else:
                    test_part = part
                
                # 如果累积部分不太长，继续累积
                if len(test_part.split()) < 15:  # 少于15个单词
                    current_part = test_part
                else:
                    if current_part:
                        sentences.append(current_part.strip())
                    current_part = part
            
            if current_part:
                sentences.append(current_part.strip())
        else:
            sentences.append(sent)
    
    # 如果还是没有分割出来，按单词数量强制分割
    if len(sentences) <= 1:
        words = segment_text.split()
        chunk_size = 10  # 每个片段10个单词
        sentences = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            if chunk:
                sentences.append(chunk)
    
    # 按字符比例分配时间
    total_chars = sum(len(s) for s in sentences)
    result = []
    current_time = start_time
    
    for i, sentence in enumerate(sentences):
        if total_chars > 0:
            sentence_duration = (len(sentence) / total_chars) * duration
        else:
            sentence_duration = duration / len(sentences)
        
        sentence_end = current_time + sentence_duration
        
        # 确保最后一个片段的结束时间精确
        if i == len(sentences) - 1:
            sentence_end = end_time
        
        result.append({
            'start': round(current_time, 2),
            'end': round(sentence_end, 2),
            'text': sentence.strip()
        })
        
        current_time = sentence_end
    
    return result


def generate_caption(audio_path):
    """
    使用 Faster-Whisper 为给定的音频文件生成英文字幕（词级时间戳）
    
    Args:
        audio_path (str): 音频文件路径
    
    Returns:
        tuple: (caption_path, caption_text) 字幕文件路径和文本内容
    """
    try:
        # 1. 检查音频文件是否存在
        if not audio_path or not os.path.exists(audio_path):
            print(f"ERROR: Audio file not found: {audio_path}")
            return None, None
        
        file_size = os.path.getsize(audio_path)
        print(f"Audio file: {audio_path} ({file_size / 1024 / 1024:.2f} MB)")
        
        # 2. 加载 Faster-Whisper 模型
        print("Loading Faster-Whisper model (small, CPU int8)...")
        model = WhisperModel("small", device="cpu", compute_type="int8")
        print("Model loaded successfully")

        print("Generating English subtitles with Faster-Whisper (word timestamps)...")
        segments_iter, info = model.transcribe(
                audio_path, 
            language="en",
            task="transcribe",
            word_timestamps=True,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=300),
        )

        # 收集段与文本
        collected_segments = []
        text_parts = []
        for seg in segments_iter:
            seg_text = (seg.text or "").strip()
            if seg_text:
                text_parts.append(seg_text)
            words = []
            if getattr(seg, "words", None):
                for w in seg.words:
                    words.append({
                        'word': w.word,
                        'start': round((w.start or 0.0), 2),
                        'end': round((w.end or 0.0), 2),
                    })
            collected_segments.append({
                'id': seg.id,
                'start': round((seg.start or 0.0), 2),
                'end': round((seg.end or 0.0), 2),
                'text': seg_text,
                'words': words,
            })

        caption_text = " ".join(text_parts).strip()
        print(f"Transcription successful: {len(caption_text)} characters")

        # 从音频路径生成字幕文件的路径
        captions_dir = current_app.config['CAPTIONS_DIR']
        base_filename = os.path.basename(audio_path)
        filename_without_ext = os.path.splitext(base_filename)[0]
        caption_path = os.path.join(captions_dir, f"{filename_without_ext}.txt")

        # 将识别出的文本写入文件
        with open(caption_path, 'w', encoding='utf-8') as f:
            f.write(caption_text)
        
        # 保存带时间戳的字幕数据（用于影子跟读）
            json_path = os.path.join(captions_dir, f"{filename_without_ext}_segments.json")
            
        # 基于词级时间戳：先按静音边界补充句号，再严格以句号断句
        SILENCE_SENTENCE_GAP = 0.6  # 视为句子边界的静音阈值（秒）

        # 汇总所有词（按时间顺序）
        all_words = []
        for seg in collected_segments:
            for w in seg['words']:
                # 复制一份，避免修改原始结构
                all_words.append({
                    'word': w['word'],
                    'start': w['start'],
                    'end': w['end'],
                })

        # 先用 LLM 恢复句末标点；若失败再退化为 LLM 边界索引；再失败退化为原生句点断句
        tokens_only = [w['word'] for w in all_words]
        break_indices = []
        punct_tokens = restore_sentence_final_punct_by_llm(tokens_only)
        if punct_tokens is not None and len(punct_tokens) == len(tokens_only):
            # 更新词文本为带句末标点的版本，并直接以标点作为断句依据
            for i, t in enumerate(punct_tokens):
                all_words[i]['word'] = t
                if t.rstrip().endswith('.') or t.rstrip().endswith('!') or t.rstrip().endswith('?'):
                    break_indices.append(i)
        else:
            # 无法恢复标点时，改用 LLM 给出边界索引
            bi = get_sentence_break_indices_by_llm(tokens_only)
            if isinstance(bi, list):
                break_indices = bi

        sentence_segments = []
        if break_indices:
            start_idx = 0
            for bi in break_indices:
                if bi < start_idx or bi >= len(all_words):
                    continue
                sent_words = all_words[start_idx: bi + 1]
                start_time = sent_words[0]['start']
                end_time = sent_words[-1]['end']
                text = "".join(w['word'] for w in sent_words).strip()
                if text:
                    # 若边界来自 LLM 索引且末尾无标点，谨慎补 '.'（标点恢复模式下通常已具备标点）
                    if not text.endswith('.') and not text.endswith('!') and not text.endswith('?'):
                        text = text + '.'
                    sentence_segments.append({
                        'id': len(sentence_segments),
                        'start': round(start_time, 2),
                        'end': round(end_time, 2),
                        'text': text
                    })
                start_idx = bi + 1
            # 余下尾部作为最后一句（如果有）
            if start_idx < len(all_words):
                sent_words = all_words[start_idx:]
                start_time = sent_words[0]['start']
                end_time = sent_words[-1]['end']
                text = "".join(w['word'] for w in sent_words).strip()
                if text:
                    if not text.endswith('.') and not text.endswith('!') and not text.endswith('?'):
                        text = text + '.'
                    sentence_segments.append({
                        'id': len(sentence_segments),
                        'start': round(start_time, 2),
                        'end': round(end_time, 2),
                        'text': text
                    })
        else:
            # LLM 不可用时，退化为基于原始标点的断句（不做静音补句号）
            current_words = []
            def flush_sentence():
                if not current_words:
                    return
                start_time = current_words[0]['start']
                end_time = current_words[-1]['end']
                text = "".join(w['word'] for w in current_words).strip()
                if text:
                    sentence_segments.append({
                        'id': len(sentence_segments),
                        'start': round(start_time, 2),
                        'end': round(end_time, 2),
                        'text': text
                    })
                current_words.clear()
            for w in all_words:
                current_words.append(w)
                token = (w['word'] or '')
                if token.rstrip().endswith('.'):
                    flush_sentence()
            flush_sentence()

        # 插入“无字幕”静音区块，保证连贯播放
        sentence_segments.sort(key=lambda s: s['start'])
        blocks = []
        prev_end = 0.0
        MICRO_GAP_THRESHOLD = 0.9  # 小于该值的间隙视为人声停顿，直接并入

        # 可能拿到总时长
        total_duration = None
        try:
            total_duration = float(getattr(info, 'duration', None))
        except Exception:
            total_duration = None

        for seg in sentence_segments:
            gap = seg['start'] - prev_end
            if gap > 0:
                if gap < MICRO_GAP_THRESHOLD and blocks and blocks[-1].get('text') != '[无字幕]':
                    # 将微小间隙并入前一字幕块：延长前一块的结束时间到当前块开始
                    # 同时将当前块的开始时间对齐到前一块的结束，消除微小“无字幕”
                    blocks[-1]['end'] = round(seg['start'], 2)
                    seg['start'] = blocks[-1]['end']
                else:
                    blocks.append({
                        'start': round(prev_end, 2),
                        'end': round(seg['start'], 2),
                        'text': '[无字幕]'
                    })
            blocks.append(seg)
            prev_end = seg['end']

        if total_duration is not None and prev_end < total_duration:
            tail_gap = total_duration - prev_end
            if tail_gap > 0:
                blocks.append({
                    'start': round(prev_end, 2),
                    'end': round(total_duration, 2),
                    'text': '[无字幕]'
                })

        for i, b in enumerate(blocks):
            b['id'] = i

            segments_data = {
                'text': caption_text,
                'language': 'en',
            'segments': blocks
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(segments_data, f, ensure_ascii=False, indent=2)
            print(f"English subtitles with timestamps saved: {json_path}")
        print(f"  Total {len(sentence_segments)} sentences (word timestamp-based)")
        print(f"  Faster-Whisper segments: {len(collected_segments)}")
        
        print(f"字幕生成成功: {caption_path}")
        return caption_path, caption_text

    except Exception as e:
        print(f"ERROR: Caption generation failed")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        import traceback
        traceback.print_exc()
        return None, None



