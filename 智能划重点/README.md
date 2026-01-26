# 智能划重点 - V2.0

> 基于真实用户反馈迭代的智能字幕高亮系统

## 🎯 核心特性

### 1. 尊重中文语境

不像市面上简单的关键词匹配，我们的算法**理解中文**：

| 其他工具 ❌ | 智能划重点 ✅ |
|------------|--------------|
| 高亮"大"（破坏"大家"） | 高亮完整"大家" |
| 高亮"很"（破坏"很多"） | 高亮完整"很多" |
| 高亮"会"（破坏"不会"） | 高亮完整"不会" |

### 2. 精准控制

**每行最多2个高亮**，避免满屏黄字的尴尬：

```
❌ 剪映风格：然后很多细心的朋友可以注意到
              ↑↑ ↑↑ ↑↑  过度高亮

✅ 智能划重点：然后很多细心的朋友可以注意到
                ↑↑ ↑↑  恰到好处
```

### 3. 上下文感知

不孤立判断单行，结合前后文选择最重要的词。

### 4. 视觉一致性

- 默认文字：白色 24pt 黑描边
- 高亮关键词：**黄色 28pt 加粗黑描边**

## 📊 技术亮点

### 中文分词引擎

使用 jieba + 自定义词典，精准识别：
- ✅ 固定搭配："能建起来"、"群山环绕"
- ✅ 成语短语："无论是"、"有一种"
- ✅ 否定结构："不会"、"不用"

### 多维度评分系统

| 维度 | 权重 | 示例 |
|------|------|------|
| 词语类别 | 10-40分 | 强调词"非常"=40分 |
| 固定搭配 | +15分 | "能建起来"+15 |
| 词语长度 | ×2分 | 4字词=8分 |
| 词性 | +5分 | 名词、形容词 |

### 智能过滤

自动过滤90+个功能词：
- 助词：的、了、呢、啊
- 代词：这、那、我、你
- 连接词：然后、或者、所以

## 🚀 快速开始

### 安装依赖

```bash
pip install jieba
```

### 使用方法

```python
from smart_highlight import analyze_subtitles, generate_ass_subtitle

# 1. 分析字幕
analysis = analyze_subtitles('video.srt')

# 2. 生成ASS字幕
generate_ass_subtitle(analysis, 'video_highlight.ass')

# 3. 烧录到视频
ffmpeg -i video.mp4 -vf "ass=video_highlight.ass" output.mp4
```

或直接使用 Claude Code Skill：

```
/videocut:智能划重点
```

## 📁 文件说明

```
智能划重点/
├── SKILL.md                    # Skill 配置（Claude Code 用）
├── README.md                   # 本文档
├── smart_highlight.py          # 核心脚本
└── tips/
    └── 智能划重点方法论.md     # 详细算法文档
```

## 🔧 配置选项

### 自定义关键词类别

编辑 `smart_highlight.py`：

```python
KEYWORD_CATEGORIES = {
    '你的类别': {
        'keywords': ['关键词1', '关键词2'],
        'priority': 3  # 1-4，数字越大越优先
    }
}
```

### 自定义高亮样式

```python
# 修改颜色（BGR格式）
highlight_tag = r'{\fs28\c&H00FFFF&\b1}'  # 黄色
# 改为红色：
highlight_tag = r'{\fs28\c&H0000FF&\b1}'

# 修改字号
highlight_tag = r'{\fs32\c&H00FFFF&\b1}'  # 32pt
```

### 自定义每行高亮数量

```python
# 默认最多2个
selected = [word for word, score in candidates[:2]]

# 改为最多3个
selected = [word for word, score in candidates[:3]]
```

## 📚 算法详解

详见 [智能划重点方法论.md](tips/智能划重点方法论.md)

包含：
- 中文分词策略
- 关键词评分算法
- 固定搭配识别
- ASS字幕生成
- 实战案例分析

## 🐛 已知问题

### Q: 专有名词被拆分了？

**解决**：添加到 jieba 用户词典

```python
import jieba
jieba.add_word('钉钉AI')
jieba.add_word('你的专有名词')
```

### Q: 某些词不应该高亮？

**解决**：添加到禁用词列表

```python
STOP_WORDS.add('你不想高亮的词')
```

### Q: 字幕太小/太大？

**原因**：视频分辨率不同，字幕自适应缩放

**解决**：调整基础字号

```python
Style: Default,PingFang SC,32,&H00FFFFFF,...  # 改为32pt
```

## 📈 版本历史

### V2.0 (2026-01-26)

**基于真实用户反馈的重大改进**

✅ **新增**：
- 固定搭配识别（"大家"、"很多"、"不会"、"能建起来"）
- 上下文感知选词
- 每行严格限制≤2个高亮
- 转录错误自动修复

✅ **修复**：
- 字体大小兼容性问题（移除PlayResX/Y）
- 词语边界识别错误
- 过度高亮问题

### V1.0 (初版)

- 基础关键词匹配
- ASS字幕生成
- FFmpeg 烧录集成

## 🤝 贡献

基于 [@Kora](https://github.com/yourusername) 的真实使用反馈开发。

**反馈渠道**：
- GitHub Issues
- 在 Claude Code 中使用 `/videocut:自更新` 告诉 AI

## 📄 License

MIT License - 自由使用、修改、分发

## 🙏 致谢

感谢：
- **jieba** - 中文分词
- **FFmpeg** - 视频处理
- **libass** - ASS字幕渲染
- **用户 Kora** - 详细反馈和测试

---

**下一步计划**：
- [ ] 机器学习个性化推荐
- [ ] 多风格主题支持（抖音/小红书/B站）
- [ ] 自动主题识别
- [ ] 动态调整高亮强度
