"""
调试Whisper segments的分割和时间映射过程
"""
import json

# 加载Whisper原始结果
with open('whisper_raw_result.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

print("="*100)
print("步骤1: Whisper原始返回数据")
print("="*100)
print(f"\n完整文本长度: {len(result['text'])} 字符")
print(f"原始Segments数量: {len(result['segments'])}")
print("\n原始Segments列表:")
for i, seg in enumerate(result['segments']):
    print(f"\n  [{i}] {seg['start']:.2f}s - {seg['end']:.2f}s ({seg['end']-seg['start']:.2f}s)")
    print(f"      文本: '{seg['text']}'")
    print(f"      Token数: {len(seg['tokens'])}, 置信度: {seg['avg_logprob']:.3f}")

print("\n" + "="*100)
print("步骤2: 按标点符号(.!?)重新分割完整文本")
print("="*100)

caption_text = result['text']
full_text = caption_text.strip()

# 按句子标点分割完整文本
sentences = []
current_start = 0

for i, char in enumerate(full_text):
    if char in '.!?':
        sentence = full_text[current_start:i+1].strip()
        if sentence:
            sentences.append({
                'text': sentence,
                'char_start': current_start,
                'char_end': i + 1
            })
            print(f"\n句子 {len(sentences)-1}:")
            print(f"  字符位置: [{current_start}:{i+1}]")
            print(f"  文本: '{sentence}'")
        current_start = i + 1

# 处理最后的非句子部分
if current_start < len(full_text):
    remaining = full_text[current_start:].strip()
    if remaining:
        sentences.append({
            'text': remaining,
            'char_start': current_start,
            'char_end': len(full_text)
        })
        print(f"\n句子 {len(sentences)-1} (无结束标点):")
        print(f"  字符位置: [{current_start}:{len(full_text)}]")
        print(f"  文本: '{remaining}'")

print(f"\n总共分割出 {len(sentences)} 个句子")

print("\n" + "="*100)
print("步骤3: 构建字符位置→时间的映射表")
print("="*100)

char_to_time = []
current_pos = 0

print("\n从Whisper原始segments构建映射:")
for seg_idx, seg in enumerate(result['segments']):
    seg_text = seg['text'].strip()
    seg_len = len(seg_text)
    seg_duration = seg['end'] - seg['start']
    
    print(f"\nSegment {seg_idx}: '{seg_text}'")
    print(f"  字符范围: [{current_pos}:{current_pos+seg_len}] (长度={seg_len})")
    print(f"  时间范围: [{seg['start']:.2f}s - {seg['end']:.2f}s] (时长={seg_duration:.2f}s)")
    print(f"  每字符时长: {seg_duration/seg_len:.4f}s")
    
    # 为这个segment的每个字符建立时间映射
    for i in range(seg_len):
        char_time = seg['start'] + (i / seg_len) * seg_duration
        char_to_time.append({
            'pos': current_pos + i,
            'time': char_time,
            'char': seg_text[i] if i < len(seg_text) else ' '
        })
    
    current_pos += seg_len + 1  # +1 for space between segments

print(f"\n总共建立了 {len(char_to_time)} 个字符的时间映射")
print(f"映射前10个字符示例:")
for i in range(min(10, len(char_to_time))):
    ct = char_to_time[i]
    print(f"  位置{ct['pos']}: '{ct['char']}' -> {ct['time']:.3f}s")

print("\n" + "="*100)
print("步骤4: 为重新分割的句子分配时间戳")
print("="*100)

segments_list = []

for idx, sentence in enumerate(sentences):
    # 找到句子的起始和结束时间
    start_time = None
    end_time = None
    
    print(f"\n处理句子 {idx}: '{sentence['text'][:50]}...'")
    print(f"  字符范围: [{sentence['char_start']}:{sentence['char_end']}]")
    
    # 查找匹配的时间
    for ct in char_to_time:
        if start_time is None and ct['pos'] >= sentence['char_start']:
            start_time = ct['time']
            print(f"  找到开始时间: {start_time:.2f}s (字符位置 {ct['pos']})")
        if ct['pos'] <= sentence['char_end']:
            end_time = ct['time']
    
    if end_time is not None:
        print(f"  找到结束时间: {end_time:.2f}s")
    
    # 如果找不到精确映射，使用整体比例估算
    if start_time is None:
        start_time = 0.0
        print(f"  [!] 未找到开始时间，使用默认值: 0.0s")
    if end_time is None:
        end_time = result['segments'][-1]['end']
        print(f"  [!] 未找到结束时间，使用最后segment的结束时间: {end_time:.2f}s")
    
    segments_list.append({
        'id': idx,
        'start': round(start_time, 2),
        'end': round(end_time, 2),
        'text': sentence['text']
    })
    
    print(f"  [OK] 最终时间戳: [{round(start_time, 2)}s - {round(end_time, 2)}s] (时长={round(end_time-start_time, 2)}s)")

print("\n" + "="*100)
print("步骤5: 最终结果对比")
print("="*100)

print(f"\n原始Whisper Segments: {len(result['segments'])} 个")
print(f"处理后的Segments: {len(segments_list)} 个")

print("\n前3个句子的对比:")
for i in range(min(3, len(segments_list))):
    seg = segments_list[i]
    print(f"\n句子 {i}:")
    print(f"  时间: {seg['start']}s - {seg['end']}s")
    print(f"  文本: '{seg['text']}'")

# 保存调试结果
output = {
    'original_segments_count': len(result['segments']),
    'processed_segments_count': len(segments_list),
    'char_to_time_mappings': len(char_to_time),
    'segments': segments_list
}

with open('debug_segments_output.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("\n" + "="*100)
print("调试结果已保存到: debug_segments_output.json")
print("="*100)

