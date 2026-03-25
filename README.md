# 视频全自动剪辑 Skill / VideoCLip-AI_2026.03.25

> Claude Skill-powered video editing toolkit - Automatic video editing


https://github.com/user-attachments/assets/2e4b7344-0589-44e9-9fdf-132478398a7e



## 谁在用？

- 📚 **知识博主**（讲课、读书分享）
- 🎓 **在线教师**（录课、教程）
- 🎬 **Vlogger**（旅行、生活记录）
- 💼 **产品经理**（产品介绍、演示）
- 🎙️ **播客主播**（长音频转视频）




## Skill 核心功能清单

| Skill | 功能 | 触发词 |
|-------|------|--------|
| `videocut:安装` | 环境准备、模型下载 | 安装、初始化 |
| `videocut:剪口播` | 转录 + 口误/静音识别 → 审查稿 | 剪口播、处理视频 |
| `videocut:剪辑` | 执行 FFmpeg 剪辑 + 循环审查 | 执行剪辑、确认 |
| `videocut:字幕` | 字幕生成与烧录（含字体预览选择） | 加字幕、生成字幕 |
| `videocut:智能划重点` | 字幕关键词智能高亮 | 智能划重点、划重点、高亮字幕 |
| `videocut:自更新` | 从错误中学习，更新规则 | 更新规则、记录反馈 |


### 🔄 自更新

从错误中学习，越用越懂你的剪辑习惯并为你update



-----------------------------------------------

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



-----------------------------------------------

## 完整工作流

```
剪口播 → 转录 + 识别 → 审查稿
    ↓
【用户确认】
    ↓
剪辑 → 执行删除 → 重新审查 → 循环直到零口误
    ↓
字幕 → Whisper 转录 → 词典纠错 → 【询问智能划重点】
    ├─ 是 → 智能高亮字幕
    └─ 否 → 纯白色字幕
    ↓
字体三选一 → 生成3张预览截图 → 【用户选择】
    ├─ 1. 苹方（简洁白字）
    ├─ 2. 中华薪火体（半透明底条）
    └─ 3. 思源宋体 Bold（描边加粗）
    ↓
烧录字幕 → 自动清理临时文件
    ↓
【完成】带字幕的视频
```
-----------------------------------------------

## V3.0 新特性

### 🆕 字体三选一预览

**烧录前可视化选择字体风格**

- 🖼️ 从视频首帧生成 3 张字体预览截图，直观对比
- 🔤 三种字体风格：苹方简洁 / 复古字体 / 思源优雅
- 📐 分辨率自适应字号（1080p → 50pt，720p → 24pt）

### ✨ 智能划重点

**超越剪映的字幕高亮，更懂中文**

1. **尊重中文语境**
   - 识别固定搭配（"大家"、"很多"、"不会"）
   - 不拆分词语边界
   - 识别成语和动词短语（"能建起来"、"群山环绕"）

2. **精准控制**
   - 每行最多 2 个高亮
   - 多维度评分系统（类别 + 词性 + 长度）
   - 上下文感知（考虑前后行）


-----------------------------------------------

**特别感谢**：
- [@Kora](https://github.com/cocolayuan) - 详细的使用反馈和测试
- [FunASR](https://github.com/alibaba-damo-academy/FunASR) - 中文语音识别
- [Whisper](https://github.com/openai/whisper) - 语音转文字
- [jieba](https://github.com/fxsjy/jieba) - 中文分词



### 🐛 Bug 报告 ｜ 💡 功能建议
- 📧 邮件：cocolaYuan@gmail.com


