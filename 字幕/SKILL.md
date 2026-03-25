---
name: videocut:字幕
description: 字幕生成与烧录。转录→词典纠错→审核→智能划重点询问→烧录。触发词：加字幕、生成字幕、字幕
---

# 字幕

> 转录 → 纠错 → 审核 → 匹配 → 【询问智能划重点】→ 【字体三选一】→ 烧录

## 流程

```
1. 转录视频（Whisper）
    ↓
2. 词典纠错 + 分句
    ↓
3. 输出字幕稿（纯文本，一句一行）
    ↓
【用户审核修改】
    ↓
4. 用户给回修改后的文本
    ↓
5. 我匹配时间戳 → 生成 SRT
    ↓
【⚡ 必须询问用户】是否需要"智能划重点"高亮字幕？
    ├─ 是 → 调用智能划重点算法 → 生成 ASS 字幕（黄色高亮关键词）
    └─ 否 → 使用普通 SRT 字幕（纯白色，无高亮）
    ↓
6. 【字体三选一】提取第一帧 → 分别用3种字体烧录预览 → 展示3张截图 → 用户选择
    ↓
7. 烧录字幕（FFmpeg，使用用户选择的字体样式）
```

## ⚡ 重要：智能划重点询问（必须执行）

**在生成 SRT 后、烧录前，必须使用 AskUserQuestion 询问用户**：

### 询问示例

问题：**"字幕已准备好，是否需要添加智能划重点效果？"**

选项1：**"是，添加智能高亮（推荐）"**
- 说明：关键词用黄色28pt加粗显示，类似剪映划重点
- 特点：尊重中文语境，每行最多2个高亮，智能识别固定搭配

选项2：**"否，使用纯白色字幕"**
- 说明：所有字幕统一白色24pt，无高亮效果
- 特点：适合正式场合或个人偏好简洁风格

### 根据用户选择执行

**如果用户选择"是"**：
1. 使用 Python 运行 `~/.claude/skills/videocut/智能划重点/smart_highlight.py`
2. 传入 SRT 文件路径作为参数
3. 脚本会自动：
   - 分析字幕，识别关键词
   - 生成 ASS 字幕文件（带高亮标记）
4. **接下来进入"字体三选一"流程**（见下方章节）
5. 根据用户选择的字体，修改 ASS 中的 Style 行，再烧录：
   ```bash
   ffmpeg -i video.mp4 -vf "ass=subtitle_highlight.ass:fontsdir=/Users/kora/Library/Fonts/" \
     -c:v libx264 -crf 23 -c:a copy output_智能划重点.mp4
   ```

**如果用户选择"否"**：
1. **接下来进入"字体三选一"流程**（见下方章节）
2. 如果选了字体1（PingFang），直接用 SRT 烧录：
   ```bash
   ffmpeg -i video.mp4 -vf "subtitles=subtitle.srt" \
     -c:v libx264 -crf 23 -c:a copy output_字幕.mp4
   ```
3. 如果选了字体2或字体3，需生成 ASS（应用对应字体 Style），再烧录：
   ```bash
   ffmpeg -i video.mp4 -vf "ass=subtitle.ass:fontsdir=/Users/kora/Library/Fonts/" \
     -c:v libx264 -crf 23 -c:a copy output_字幕.mp4
   ```

---

## ⚡ 字体三选一（必须执行）

**在确定字幕类型（普通/划重点）后、烧录前，必须让用户选择字体样式。**

### 步骤

1. **提取第一帧**（带第一句字幕的时间点）：
   ```bash
   ffmpeg -ss <第一句字幕开始时间> -i video.mp4 -vframes 1 -q:v 2 _preview_frame.png
   ```

2. **生成3个临时 ASS 文件**（每个对应一种字体样式），写入第一句字幕（如已选智能高亮则带高亮标记，如选纯白则全白色），然后烧录到帧图上：

   ```bash
   # 预览1 — PingFang
   ffmpeg -y -i _preview_frame.png -vf "ass=_preview_font1.ass:fontsdir=/System/Library/Fonts/" -frames:v 1 _preview_font1.png
   # 预览2 — 中华薪火体
   ffmpeg -y -i _preview_frame.png -vf "ass=_preview_font2.ass:fontsdir=/Users/kora/Library/Fonts/" -frames:v 1 _preview_font2.png
   # 预览3 — 思源宋体
   ffmpeg -y -i _preview_frame.png -vf "ass=_preview_font3.ass:fontsdir=/Users/kora/Library/Fonts/" -frames:v 1 _preview_font3.png
   ```
   > 预览 ASS 文件使用上方"三种字体的 ASS 样式定义"中对应的 Style 行。FontSize 根据视频分辨率自适应。

3. **展示预览并询问用户**，使用 AskUserQuestion：

   问题：**"请选择字幕字体样式（预览图见上方）："**

   选项1：**"苹方 PingFang — 圆润现代，经典默认"**
   选项2：**"中华薪火体 — 手写风格，带黑色底条"**
   选项3：**"思源宋体 — 衬线加粗，复古正式"**

   > 展示预览图时，先用 Read 工具读取3张 PNG 让用户看到效果。

### 分辨率自适应字号

烧录前先检测视频分辨率，根据高度决定字号：

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 video.mp4
```

| 分辨率 | PlayResY | FontSize | Outline/Shadow 缩放 |
|--------|----------|----------|---------------------|
| 1080p（height≥1080） | 1080 | **50** | 按下方1080p值 |
| 720p（height<1080）  | 720  | **24** | 按比例缩小约50% |

> 以下样式均以 **1080p** 为例。720p 时 FontSize 改为 24，Outline/Shadow 等比缩小。

### 三种字体的 ASS 样式定义

#### 字体1：PingFang（苹方）— 现有默认

**普通字幕**（1080p）：
```
Style: Default,PingFang SC,50,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,0,2,10,10,50,1
```
**划重点高亮**：
```ass
{\c&H00FFFF&\b1}高亮词{\r}
```

#### 字体2：中华薪火体 — 带黑色半透明底条

**字体路径**：`/Users/kora/Library/Fonts/中华薪火体.ttf`

**普通字幕**（1080p，BorderStyle=3 实现底条效果）：
```
Style: Default,中华薪火体,50,&H00FFFFFF,&H000000FF,&H80000000,&H80000000,0,0,0,0,100,100,2,0,3,8,0,2,10,10,50,1
```
- `BorderStyle=3`：使用 OutlineColour 作为背景框填充色
- `OutlineColour=&H80000000`：黑色 50% 透明度底条（rgba(0,0,0,0.50)）
- `Outline=8`：四周均匀 padding（⚠️ 不要用 Shadow，Shadow 只往右下偏移）
- `Shadow=0`
- `Spacing=2`：字间距

**划重点高亮**：
```ass
{\c&H1DF4FF&\b1}高亮词{\r}
```
> 注意：ASS 颜色为 BGR 格式，CSS `#FFF41D` → ASS `&H1DF4FF&`

#### 字体3：思源宋体 Bold — 衬线描边

**字体路径**：`/Users/kora/Library/Fonts/SourceHanSerifCN-Bold.ttf`

**普通字幕**（1080p）：
```
Style: Default,Source Han Serif CN,50,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2.8,0,1,3,0,2,10,10,50,1
```
- Bold=-1，Spacing=2.8，描边3px黑色

**划重点高亮**：
```ass
{\c&H1DF4FF&\b1}高亮词{\r}
```
> 高亮时加粗（b1），颜色 `#FFF41D` → `&H1DF4FF&`

### 根据字体选择烧录

**ASS 字幕**（划重点 或 需要特殊字体样式时）：
```bash
ffmpeg -i video.mp4 -vf "ass=subtitle.ass:fontsdir=/Users/kora/Library/Fonts/" \
  -c:v libx264 -crf 23 -c:a copy output.mp4
```
> `fontsdir` 确保 FFmpeg 能找到自定义字体文件。

**SRT 字幕 + 自定义字体**（普通字幕 + 非PingFang字体时，需转为 ASS）：
- 即使用户选择"否"（不划重点），如果选了字体2或字体3，也需要生成 ASS 来指定字体样式
- 只有选择字体1（PingFang）+ 不划重点时，才直接用 SRT 烧录

### ⚠️ 烧录完成后清理临时文件（必须执行）

烧录成功后，删除所有中间产物，只保留**原视频**和**成品视频**：

```bash
rm -f 视频名.json 视频名.srt 视频名_highlight.ass 视频名_keywords.json \
      _preview_frame.png _preview_font*.png _pf*.ass
```

**保留**：
- `原视频.MP4` — 原始素材
- `原视频_智能划重点.mp4` 或 `原视频_字幕.mp4` — 最终成品

**删除**：
- `*.json` — Whisper 转录 JSON
- `*.srt` — SRT 字幕文件
- `*.ass` — ASS 字幕文件
- `_preview_*` — 字体预览临时图片

---

## 转录

使用 OpenAI Whisper 模型进行语音转文字：

```bash
whisper video.mp4 --model large-v3 --language zh --output_format json
```

| 模型 | 用途 |
|------|------|
| `large-v3` | 默认，高精度 |
| `medium` | 较快，准确率稍低 |

输出 JSON 包含逐词时间戳，用于后续 SRT 生成。

---

## ⚠️ 时间戳规则（强制）

**禁止按字数比例估算时间戳！必须从转录 JSON 读取每个字符的实际时间。**

```python
# ❌ 错误：按比例估算
line_duration = (len(line) / total_chars) * duration
start_time = current_time
end_time = current_time + line_duration

# ✅ 正确：从转录 JSON 读取实际时间戳
start_time = chars[start_idx]['start']  # 第一个字的开始时间
end_time = chars[end_idx]['end']        # 最后一个字的结束时间
```

### 为什么不能估算？

| 估算方式 | 实际时间 | 偏差 |
|----------|----------|------|
| 按比例：19.17s | 实际：21.29s | **2秒** |

2秒的偏差会导致字幕明显不同步，用户体验极差。

---

## 字幕规范

| 规则 | 说明 |
|------|------|
| 一屏一行 | 不换行，不堆叠 |
| ≤15字/行 | 超过15字必须拆分（4:3竖屏） |
| 句尾无标点 | `你好` 不是 `你好。` |
| 句中保留标点 | `先点这里，再点那里` |

---

## 词典纠错

读取 `词典.txt`，每行一个正确写法：

```
skills
Claude
iPhone
```

我自动识别变体：`claude` → `Claude`

---

## 字幕稿格式

**我给用户的**（纯文本，≤15字/行）：

```
今天给大家分享一个技巧
很多人可能不知道
其实这个功能
藏在设置里面
你只要点击这里
就能看到了
```

**用户修改后给回我**，我再匹配时间戳生成 SRT。

---

## 样式说明

### 普通字幕（用户选择"否"）

- 字体：50pt 白色（1080p）/ 24pt（720p）
- 描边：黑色
- 位置：底部居中
- 格式：ASS（需要支持字体选择）

### 智能划重点字幕（用户选择"是"）

- 默认文字：50pt 白色（1080p）/ 24pt（720p）
- 高亮关键词：黄色（`&H1DF4FF&`）加粗
- 位置：底部居中
- 格式：ASS（支持内联样式）

**高亮规则**：
- 每行最多2个高亮
- 尊重中文固定搭配（"大家"、"很多"、"不会"、"能建起来"）
- 智能优先级（强调词 > 核心名词 > 形容词）
- 自动过滤90+功能词

---

## 输出文件

### 用户选择"否"（纯白字幕）

```
视频名_字幕稿.txt   # 纯文本，用户编辑后的
视频名.srt          # SRT 字幕文件
视频名_字幕.mp4     # 带纯白色字幕的视频
```

### 用户选择"是"（智能划重点）

```
视频名_字幕稿.txt          # 纯文本，用户编辑后的
视频名.srt                 # SRT 字幕文件（原始）
视频名_keywords.json       # 关键词分析结果
视频名_highlight.ass       # ASS 字幕（带高亮）
视频名_智能划重点.mp4      # 带高亮字幕的视频
```

---

## 常见问题

### Q1: 什么时候选"智能划重点"？

**推荐场景**：
- ✅ 教程视频、知识分享
- ✅ 产品介绍、营销视频
- ✅ Vlog、旅行记录
- ✅ 需要强调重点的内容

**不推荐场景**：
- ❌ 正式会议记录
- ❌ 严肃纪录片、访谈
- ❌ 个人偏好简洁风格

### Q2: 能否后期修改选择？

可以！

**如果选了"否"但想添加高亮**：
```
/videocut:智能划重点
```
AI 会读取已有的 SRT，生成带高亮的版本。

**如果选了"是"但想要纯白色**：
保留原始 SRT 文件，用它重新烧录即可。

### Q3: 智能划重点会影响字幕内容吗？

**不会！** 只改变视觉样式（颜色、大小、加粗），文字内容完全一致。

### Q4: 能自定义高亮颜色吗？

可以！编辑 `~/.claude/skills/videocut/智能划重点/smart_highlight.py`：

```python
# 黄色（默认）
highlight_tag = r'{\c&H1DF4FF&\b1}'

# 改为红色
highlight_tag = r'{\c&H0000FF&\b1}'

# 改为绿色
highlight_tag = r'{\c&H00FF00&\b1}'
```

---

## 反馈记录

### 2026-01-27
- **字幕不同步（00:10-00:24区间）**
  - 原因：按字数比例估算时间戳
  - 正确：必须从转录 JSON 读取每个字符的实际 start/end 时间
  - **教训**：绝不估算，只用实际转录时间戳
