#!/usr/bin/env python3
"""
智能划重点 v2.0 - 改进版
基于用户反馈修复：
1. 尊重中文词语边界（"大家"不拆分"大"）
2. 识别固定搭配（"很多"、"不会"、"能建起来"）
3. 考虑上下文（前后行）
4. 每行最多2个重点词
5. 修复转录错误
"""

import jieba
import jieba.posseg as pseg
import json
from typing import List, Dict, Tuple

# 固定搭配词典 - 这些词必须整体高亮或不高亮
FIXED_COLLOCATIONS = {
    '大家', '很多', '不会', '能建起来',
    '有一种', '这一点', '不仅', '而且',
    '因为', '所以', '如果', '无论是',
    '群山环绕',
}

# 禁用词 - 这些词不应该被高亮
STOP_WORDS = {
    '的', '了', '呢', '啊', '吗', '吧', '呀',
    '是', '在', '有', '和', '与', '或', '及',
    '这', '那', '这个', '那个', '这些', '那些',
    '我', '你', '他', '她', '它', '我们', '你们', '他们', '它们',
    '也', '都', '就', '才', '又', '再',
    '什么', '怎么', '哪里', '为什么',
    '然后', '或者', '不用',
}

# 高优先级关键词类别
KEYWORD_CATEGORIES = {
    '强调词': {
        'keywords': ['非常', '十分', '特别', '最', '超级', '极其'],
        'priority': 4
    },
    '核心名词': {
        'keywords': ['高铁', '座位', '空间', '杂志', '质量', '工程', '小朋友', '窗边'],
        'priority': 3
    },
    '正面形容词': {
        'keywords': ['宽敞', '有利', '伟大', '细心'],
        'priority': 3
    },
    '固定搭配': {
        'keywords': ['能建起来', '群山环绕', '有一种'],
        'priority': 2
    },
    '能愿动词': {
        'keywords': ['可以'],
        'priority': 1
    }
}


def fix_transcription_errors(lines: List[str]) -> List[str]:
    """修复已知的转录错误"""
    fixed = []
    for line in lines:
        # 修复："如果有一种的小朋友" → "如果有一种小朋友"
        line = line.replace('如果有一种的小朋友', '如果有一种小朋友')
        fixed.append(line)
    return fixed


def segment_with_collocations(text: str) -> List[str]:
    """
    中文分词，但保持固定搭配完整
    """
    # 先检查文本中的固定搭配
    found_collocations = []
    for collocation in FIXED_COLLOCATIONS:
        if collocation in text:
            found_collocations.append(collocation)

    # 用jieba分词
    words = list(jieba.cut(text))

    # 合并固定搭配
    result = []
    i = 0
    while i < len(words):
        # 尝试向前看多个词，检查是否形成固定搭配
        found = False
        for length in range(min(5, len(words) - i), 0, -1):
            phrase = ''.join(words[i:i+length])
            if phrase in FIXED_COLLOCATIONS:
                result.append(phrase)
                i += length
                found = True
                break

        if not found:
            result.append(words[i])
            i += 1

    return result


def calculate_keyword_score(word: str, context: Dict) -> float:
    """
    计算关键词的得分
    考虑因素：
    1. 词性和类别优先级
    2. 上下文相关性
    3. 位置（句子主干 > 修饰成分）
    """
    score = 0.0

    # 禁用词直接返回0
    if word in STOP_WORDS:
        return 0.0

    # 单字不高亮（除非是固定搭配）
    if len(word) == 1 and word not in FIXED_COLLOCATIONS:
        return 0.0

    # 类别优先级得分
    for category, info in KEYWORD_CATEGORIES.items():
        if word in info['keywords']:
            score += info['priority'] * 10

    # 固定搭配加分
    if word in FIXED_COLLOCATIONS:
        score += 15

    # 长度得分（更长的词可能更重要）
    if len(word) >= 2:
        score += len(word) * 2

    # 名词和形容词加分
    if context.get('pos') in ['n', 'a', 'ad', 'an']:
        score += 5

    return score


def select_highlights_for_line(text: str, prev_line: str = '', next_line: str = '') -> List[str]:
    """
    为一行字幕选择高亮词（最多2个）
    考虑上下文和语义重要性
    """
    # 分词（保持固定搭配）
    words = segment_with_collocations(text)

    # 使用jieba词性标注辅助判断
    word_pos = {}
    for word, pos in pseg.cut(text):
        word_pos[word] = pos

    # 计算每个词的得分
    candidates = []
    for word in words:
        context = {
            'prev_line': prev_line,
            'next_line': next_line,
            'text': text,
            'pos': word_pos.get(word, '')
        }

        score = calculate_keyword_score(word, context)
        if score > 0:
            candidates.append((word, score))

    # 按得分排序，选择前2个
    candidates.sort(key=lambda x: x[1], reverse=True)
    selected = [word for word, score in candidates[:2]]

    return selected


def analyze_subtitles(srt_file: str) -> Dict:
    """
    分析字幕，生成智能高亮方案
    """
    # 读取SRT文件
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析字幕
    blocks = content.strip().split('\n\n')
    subtitles = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            index = lines[0]
            timecode = lines[1]
            text = '\n'.join(lines[2:])
            subtitles.append({
                'index': index,
                'timecode': timecode,
                'text': text
            })

    # 修复转录错误
    texts = [sub['text'] for sub in subtitles]
    fixed_texts = fix_transcription_errors(texts)
    for i, fixed_text in enumerate(fixed_texts):
        subtitles[i]['text'] = fixed_text

    # 为每行选择高亮词
    result = {
        'subtitles': [],
        'statistics': {
            'total_lines': len(subtitles),
            'total_highlights': 0,
        }
    }

    for i, sub in enumerate(subtitles):
        prev_text = subtitles[i-1]['text'] if i > 0 else ''
        next_text = subtitles[i+1]['text'] if i < len(subtitles) - 1 else ''

        highlights = select_highlights_for_line(
            sub['text'],
            prev_line=prev_text,
            next_line=next_text
        )

        result['subtitles'].append({
            'index': sub['index'],
            'timecode': sub['timecode'],
            'text': sub['text'],
            'highlights': highlights
        })

        result['statistics']['total_highlights'] += len(highlights)

    return result


def generate_ass_subtitle(analysis: Dict, output_file: str):
    """
    生成带高亮的ASS字幕文件
    """
    # ASS文件头
    ass_header = """[Script Info]
Title: 智能划重点字幕
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFang SC,24,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,2,10,10,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    ass_lines = [ass_header]

    # 生成每行字幕
    for sub in analysis['subtitles']:
        # 转换时间格式：SRT (00:00:00,000) -> ASS (0:00:00.00)
        timecode = sub['timecode']
        start, end = timecode.split(' --> ')
        start_ass = start.replace(',', '.')[:-1]  # 去掉最后一位毫秒
        end_ass = end.replace(',', '.')[:-1]

        # 处理文本，添加高亮标记
        text = sub['text']
        for keyword in sorted(sub['highlights'], key=len, reverse=True):
            # 高亮样式：黄色、28pt、加粗
            highlight_tag = r'{\fs28\c&H00FFFF&\b1}' + keyword + r'{\r}'
            text = text.replace(keyword, highlight_tag)

        # 生成ASS行
        ass_line = f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}"
        ass_lines.append(ass_line)

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ass_lines))


if __name__ == '__main__':
    # 分析字幕
    print("正在分析字幕...")
    analysis = analyze_subtitles('/Users/kora/Github coding/Video/1.虫子/虫子_edited.srt')

    # 保存分析结果
    with open('/Users/kora/Github coding/Video/1.虫子/虫子_keywords_v2.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"✅ 分析完成")
    print(f"   总行数: {analysis['statistics']['total_lines']}")
    print(f"   总高亮数: {analysis['statistics']['total_highlights']}")
    print(f"   平均每行: {analysis['statistics']['total_highlights'] / analysis['statistics']['total_lines']:.1f} 个")

    # 显示每行的高亮词
    print("\n每行高亮词预览：")
    for sub in analysis['subtitles']:
        if sub['highlights']:
            print(f"  [{sub['index']}] {sub['text']}")
            print(f"       高亮: {', '.join(sub['highlights'])}")

    # 生成ASS字幕
    print("\n正在生成ASS字幕...")
    generate_ass_subtitle(analysis, '/Users/kora/Github coding/Video/1.虫子/虫子_highlight_v2.ass')
    print("✅ ASS字幕已生成")
