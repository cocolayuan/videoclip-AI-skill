# 视频全自动剪辑 Skill / VideoCLip-AI

> Claude Skill-powered video editing toolkit - Automatic video editing

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai)
[![Version](https://img.shields.io/badge/version-2.0.0-green)](https://github.com/cocolayuan/videoclip-ai)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

🎬 自动剪口误、语气词、静音
📝 一键生成字幕 + 智能划重点
🤖 基于 Claude Code Skills，越用越懂你

**适用场景**：教程视频、知识分享、长播客 Vlog、AI 产品介绍

---

## 为什么选择视频全自动剪辑？

**3 分钟剪完 30 分钟视频** - AI 自动处理重复劳动，你只需审核结果

- ✅ **口误识别**：逐字检测，精准定位，一个不漏
- ✅ **智能字幕**：Whisper 转录 + 智能划重点，比剪映更懂中文
- ✅ **零学习成本**：纯文本交互，会聊天就会用

---

## 核心功能

### 🎯 剪口播

自动识别并删除：
- **口误**："这个...那个..."、重复词、卡顿
- **语气词**："嗯"、"啊"、"呃"、"哎"
- **静音片段**：≥1秒的静音自动删除

**工作流程**：
```
1. AI 转录视频（FunASR 30秒分段，逐字时间戳）
2. 智能识别口误 + 静音 + 语气词
3. 生成审查稿（Markdown 格式）
4. 你确认后，AI 自动剪辑
5. 循环审查，直到零口误
```

**实际案例**：
- 原视频：51 秒，8 处口误
- 剪辑后：47 秒，零口误
- 处理时间：3 分钟

---

### 📝 智能字幕

**Whisper 转录 + 词典纠错 + 智能划重点**

#### 转录
- 使用 OpenAI Whisper large-v3 模型
- 支持词典自动纠错（Claude → Claude，iPhone → iPhone）
- 逐词时间戳，精准匹配

#### 🆕 智能划重点（V2.0 新功能）

**类似剪映的字幕高亮，但更懂中文**

- **尊重中文语境**：
  - ✅ "大家" 整体高亮（不拆分为 "大"）
  - ✅ "很多" 保持完整（不拆分为 "很"）
  - ✅ "不会" 作为固定搭配
  - ✅ "能建起来" 动词短语整体高亮

- **智能控制**：
  - 每行最多 2 个高亮，避免过度标记
  - 智能优先级（强调词 > 核心名词 > 形容词）
  - 自动过滤 90+ 功能词（"然后"、"或者"、"的"、"了"）

- **视觉效果**：
  - 默认文字：白色 24pt，黑色描边
  - 高亮关键词：**黄色 28pt 加粗**，黑色描边

**实际案例**：
- 21 行字幕 → 38 个智能高亮
- 平均每行 1.8 个高亮
- 识别关键词：非常、高铁、座位、宽敞、质量、伟大...

---

### 🔄 自更新

从错误中学习，越用越懂你的剪辑习惯

```
/videocut:自更新

告诉 AI："'嗯哼'也应该识别为语气词"
或："'Claude'的大小写要纠正"
```

AI 会自动更新规则，下次剪辑生效。

---

## 快速开始

### 1. 安装 Claude Code

如果还没安装，访问 [Claude Code](https://claude.ai/code) 下载安装。

### 2. 克隆 Skills

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/cocolayuan/videoclip-ai.git ~/.claude/skills/videocut
```

### 3. 安装依赖

打开 Claude Code，输入：

```
/videocut:安装
```

AI 会自动安装：
- Python 依赖（FunASR、Whisper、jieba）
- FFmpeg（如果未安装）
- 下载 AI 模型（~5GB，首次较慢）

### 4. 开始剪辑

```
/videocut:剪口播
```

AI 会引导你完成整个流程。

---

## 使用示例

### 场景 1：剪教程视频

```
用户: 帮我剪这个视频的口播部分
AI: 我会为你处理...
    [转录中] 使用 FunASR...
    [分析中] 识别到 8 处口误、5 个语气词、0 处静音
    [生成审查稿]

用户: 确认删除
AI: [剪辑中] 使用 FFmpeg...
    ✅ 完成！原 51 秒 → 剪辑后 47 秒
```

### 场景 2：加字幕 + 智能划重点

```
用户: 帮剪好的视频加字幕
AI: [转录中] 使用 Whisper...
    [生成字幕稿] 请审核修改

用户: [修改后] 确认
AI: 字幕已准备好，是否需要添加"智能划重点"效果？
    选项1: 是，添加智能高亮（推荐）
    选项2: 否，使用纯白色字幕

用户: 选择 1
AI: [分析中] 识别关键词...
    [生成 ASS 字幕] 带黄色高亮
    [烧录中] 使用 FFmpeg...
    ✅ 完成！视频_智能划重点.mp4
```

---

## 完整工作流

```
剪口播 → 转录 + 识别 → 审查稿
    ↓
【用户确认】
    ↓
剪辑 → 执行删除 → 重新审查 → 循环直到零口误
    ↓
字幕 → 词典纠错 → 【询问智能划重点】
    ├─ 是 → 智能高亮字幕
    └─ 否 → 纯白色字幕
    ↓
【完成】带字幕的视频
```

---

## Skill 清单

| Skill | 功能 | 触发词 |
|-------|------|--------|
| `videocut:安装` | 环境准备、模型下载 | 安装、初始化 |
| `videocut:剪口播` | 转录 + 口误/静音识别 → 审查稿 | 剪口播、处理视频 |
| `videocut:剪辑` | 执行 FFmpeg 剪辑 + 循环审查 | 执行剪辑、确认 |
| `videocut:字幕` | 字幕生成与烧录（含智能划重点询问） | 加字幕、生成字幕 |
| `videocut:智能划重点` | 🆕 字幕关键词智能高亮 | 智能划重点、划重点、高亮字幕 |
| `videocut:自更新` | 从错误中学习，更新规则 | 更新规则、记录反馈 |

---

## 技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| **Claude Sonnet 4.5** | AI 引擎 | 理解用户意图，协调整个流程 |
| **FunASR** | 中文语音识别 | 阿里开源，字符级时间戳 |
| **Whisper large-v3** | 字幕转录 | OpenAI 模型，高精度 |
| **jieba** | 中文分词 | 智能划重点的基础 |
| **FFmpeg** | 视频处理 | 剪辑、字幕烧录 |

---

## V2.0 新特性

### 🆕 智能划重点

**类似剪映的字幕高亮，但更懂中文**

#### 核心改进（基于真实用户反馈）

1. **尊重中文语境**
   - 识别固定搭配（"大家"、"很多"、"不会"）
   - 不拆分词语边界
   - 识别成语和动词短语（"能建起来"、"群山环绕"）

2. **精准控制**
   - 每行最多 2 个高亮
   - 多维度评分系统（类别 + 词性 + 长度）
   - 上下文感知（考虑前后行）

3. **智能过滤**
   - 自动过滤 90+ 功能词
   - 禁用代词、连接词、助词

#### 技术实现

```python
# 固定搭配识别
FIXED_COLLOCATIONS = {'大家', '很多', '不会', '能建起来', ...}

# 关键词分类
KEYWORD_CATEGORIES = {
    '强调词': {'keywords': ['非常', '十分', ...], 'priority': 4},
    '核心名词': {'keywords': ['高铁', '座位', ...], 'priority': 3},
    '正面形容词': {'keywords': ['宽敞', '有利', ...], 'priority': 3},
}

# 多维度评分
score = 类别优先级 + 固定搭配加分 + 长度加分 + 词性加分
```

详见：[智能划重点方法论](智能划重点/tips/智能划重点方法论.md)

### 🔄 字幕 Skill 集成询问

**V2.0 之前**：
```
/videocut:字幕          # 生成纯白字幕
/videocut:智能划重点     # 手动调用添加高亮
```

**V2.0 之后**：
```
/videocut:字幕
  ↓ 生成 SRT 后自动询问
  ├─ 是 → 一步到位，智能高亮
  └─ 否 → 纯白字幕
```

---

## 谁在用？

- 📚 **知识博主**（讲课、读书分享）
- 🎓 **在线教师**（录课、教程）
- 🎬 **Vlogger**（旅行、生活记录）
- 💼 **产品经理**（产品介绍、演示）
- 🎙️ **播客主播**（长音频转视频）

---

## 实际案例

### 案例 1：高铁 Vlog

**原视频**：51 秒，口播介绍高铁座位
**识别结果**：
- 3 处口误
- 5 个语气词（"啊"）
- 0 处静音

**剪辑结果**：47.33 秒
**字幕高亮**：21 行 → 38 个智能高亮

**关键词示例**：
- "非常" - 强调词，高优先级
- "高铁"、"座位"、"空间" - 核心名词
- "宽敞"、"有利"、"伟大" - 正面形容词
- "能建起来"、"群山环绕" - 固定搭配

### 案例 2：教程视频

**原视频**：30 分钟，编程教程
**识别结果**：
- 47 处口误
- 23 个语气词
- 12 处静音（≥1s）

**剪辑结果**：26 分钟
**时间节省**：原本需要 2 小时手动剪辑 → 现在 5 分钟

---

## 常见问题

### Q1: 支持哪些视频格式？

支持所有 FFmpeg 支持的格式：MP4、MOV、AVI、MKV、FLV 等。

### Q2: 模型下载很慢怎么办？

模型约 5GB，首次下载较慢。建议：
- 使用国内网络环境
- 或手动下载后放到指定目录

### Q3: 能否自定义高亮颜色？

可以！编辑 `~/.claude/skills/videocut/智能划重点/smart_highlight.py`：

```python
# 黄色（默认）
highlight_tag = r'{\fs28\c&H00FFFF&\b1}'

# 改为红色
highlight_tag = r'{\fs28\c&H0000FF&\b1}'
```

### Q4: 识别错误怎么办？

使用 `/videocut:自更新` 告诉 AI，它会学习并更新规则。

### Q5: 支持英文视频吗？

目前针对中文优化。英文支持有限，建议使用其他工具。

---

## 版本历史

### V2.0.0 (2026-01-26)

**重大更新**：智能划重点功能

✨ **新增**：
- 智能划重点算法（中文语境识别）
- 字幕 Skill 集成询问功能
- 完整技术文档（700+ 行方法论）

🐛 **修复**：
- 字体大小兼容性问题
- 词语边界识别错误
- 过度高亮问题

详见：[CHANGELOG.md](CHANGELOG.md)

### V1.0.0 (2026-01-24)

🎉 **首次发布**：
- 口误识别
- 静音检测
- 语气词处理
- 字幕生成
- 自更新功能

---

## 贡献

欢迎提 Issue 和 PR！

**特别感谢**：
- [@Kora](https://github.com/cocolayuan) - 详细的使用反馈和测试
- [FunASR](https://github.com/alibaba-damo-academy/FunASR) - 中文语音识别
- [Whisper](https://github.com/openai/whisper) - 语音转文字
- [jieba](https://github.com/fxsjy/jieba) - 中文分词

### 反馈渠道

- 🐛 Bug 报告：[GitHub Issues](https://github.com/cocolayuan/videoclip-ai/issues)
- 💡 功能建议：[Discussions](https://github.com/cocolayuan/videoclip-ai/discussions)
- 📧 邮件：cocolayuan@example.com

---

## 开发路线图

### 🚀 进行中
- [ ] 智能划重点 v2.1（个性化学习）

### 💡 计划中
- [ ] 多风格主题（抖音/小红书/B站）
- [ ] 自动主题识别（美食/旅行/科技）
- [ ] 批量处理模式
- [ ] Web UI 界面

### 🔮 探索中
- [ ] 语音情绪识别（根据语气调整高亮）
- [ ] 智能分镜建议
- [ ] 背景音乐推荐

---

## 设计哲学

**"用户反馈 > 技术炫技"**

我们不追求：
- ❌ 最先进的 NLP 模型
- ❌ 最复杂的算法架构
- ❌ 最多的功能选项

我们追求：
- ✅ **真实场景下好用** - 基于实际使用反馈迭代
- ✅ **尊重用户习惯** - 理解中文语境，而非机械匹配
- ✅ **保持简单** - 90% 场景开箱即用，10% 场景可配置

---

## License

MIT License

Copyright (c) 2026 cocolayuan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=cocolayuan/videoclip-ai&type=Date)](https://star-history.com/#cocolayuan/videoclip-ai&Date)

---

**如果这个项目对你有帮助，请给个 ⭐ Star！**

**有问题或建议？欢迎提 [Issue](https://github.com/cocolayuan/videoclip-ai/issues)！**
