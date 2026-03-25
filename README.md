# 视频全自动剪辑 Skill / VideoCLip-AI

> Claude Skill-powered video editing toolkit - Automatic video editing

**适用场景**：教程视频、知识分享、长播客 Vlog、AI 产品介绍
🎬 自动剪口误、语气词、静音
📝 一键生成字幕 + 智能划重点 + 字体三选一预览，比剪映更懂中文
🤖 基于 Claude Code Skills，注重视觉效果，越用越懂你



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
| `videocut:字幕` | 字幕生成与烧录（含智能划重点询问） | 加字幕、生成字幕 |
| `videocut:智能划重点` | 🆕 字幕关键词智能高亮 | 智能划重点、划重点、高亮字幕 |
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
字幕 → 词典纠错 → 【询问智能划重点】
    ├─ 是 → 智能高亮字幕
    └─ 否 → 纯白色字幕
    ↓
【完成】带字幕的视频
```
-----------------------------------------------

## V2.0 新特性

### 🆕 智能划重点

**超越剪映的字幕高亮，但更懂中文**

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
  
     
-----------------------------------------------

**特别感谢**：
- [@Kora](https://github.com/cocolayuan) - 详细的使用反馈和测试
- [FunASR](https://github.com/alibaba-damo-academy/FunASR) - 中文语音识别
- [Whisper](https://github.com/openai/whisper) - 语音转文字
- [jieba](https://github.com/fxsjy/jieba) - 中文分词

  

### 🐛 Bug 报告 ｜ 💡 功能建议
- 📧 邮件：cocolaYuan@gmail.com


