# 升级指南

## 🎉 V3.0 - 字幕可选字体（2026-03-25）

**核心新功能**：字体三选一预览 — 烧录前生成3张截图，可视化选择字体样式

### 新增特性
- 三种字体：苹方 / 中华薪火体（带底条）/ 思源宋体 Bold
- 预览截图对比选择
- 分辨率自适应字号（1080p=50, 720p=24）
- 烧录后自动清理中间文件

### 升级步骤
```bash
cd ~/.claude/skills/videoclip-AI-skill
git pull origin main
```

无需安装新依赖，完全兼容 V2.0。

---

## V2.0 - 智能划重点（2026-01-26）

**核心新功能**：智能划重点 - 为字幕添加智能高亮，类似剪映的划重点功能

## 快速升级

### 步骤 1: 拉取最新代码

如果你是通过 git clone 安装的：

```bash
cd ~/.claude/skills/videocut
git pull origin main
```

如果你是手动下载的，重新下载并覆盖：

```bash
# 备份旧版本（可选）
mv ~/.claude/skills/videocut ~/.claude/skills/videocut.backup

# 下载新版本
git clone https://github.com/Ceeon/videocut-skills.git ~/.claude/skills/videocut
```

### 步骤 2: 安装新依赖

```bash
pip3 install jieba
```

验证安装：

```bash
python3 -c "import jieba; print('✅ jieba 已安装')"
```

### 步骤 3: 重启 Claude Code

如果 Claude Code 正在运行，重启以加载新 Skill。

### 步骤 4: 验证新功能

在 Claude Code 中输入：

```
/videocut:智能划重点
```

如果看到 Skill 被识别，说明升级成功！

## 新增功能

### 🆕 智能划重点

**使用场景**：
- 已剪辑好的视频，想添加字幕并高亮关键词
- 已有字幕文件（SRT格式），想添加智能高亮

**触发词**：
```
智能划重点
划重点
高亮字幕
```

**核心特性**：
- ✅ 尊重中文语境（"大家"、"很多"、"不会"不拆分）
- ✅ 每行最多2个高亮
- ✅ 智能优先级排序
- ✅ 自动过滤功能词

**视觉效果**：
- 默认文字：白色 24pt 黑描边
- 高亮关键词：黄色 28pt 加粗 黑描边

**示例**：
```
用户: 帮我这个视频添加智能划重点
AI: 我会为你的视频添加智能高亮字幕...
```

## 完整更新内容

### 新增文件

```
智能划重点/
├── SKILL.md                      # Skill 配置
├── README.md                     # 使用文档
├── smart_highlight.py            # 核心算法（310行）
└── tips/
    └── 智能划重点方法论.md       # 详细技术文档（700行）
```

### 修改文件

- `README.md` - 更新功能列表和工作流
- `CHANGELOG.md` - 版本历史
- `VERSION` - 版本号 2.0.0

### 新增依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| jieba | >= 0.42 | 中文分词 |

## 兼容性

### ✅ 向后兼容

V2.0 **完全兼容** V1.0 的所有功能：
- ✅ `/videocut:安装` - 无变化
- ✅ `/videocut:剪口播` - 无变化
- ✅ `/videocut:剪辑` - 无变化
- ✅ `/videocut:字幕` - 无变化
- ✅ `/videocut:自更新` - 无变化

新增的 `/videocut:智能划重点` 是**独立功能**，不影响现有工作流。

### 数据迁移

**不需要任何数据迁移**。

V1.0 生成的文件（转录JSON、审查稿、字幕等）在 V2.0 中继续有效。

## 推荐工作流更新

### 之前的工作流（V1.0）

```
剪口播 → 剪辑 → 字幕 → ✅ 完成
```

### 现在的工作流（V2.0）

```
剪口播 → 剪辑 → 字幕 → 智能划重点 → ✅ 完成
                              ↑ 新增步骤
```

## 故障排查

### Q1: "jieba 导入失败"

**问题**：
```
ImportError: No module named 'jieba'
```

**解决**：
```bash
pip3 install jieba
# 或
python3 -m pip install jieba
```

### Q2: "找不到 /videocut:智能划重点"

**问题**：Skill 未被识别

**解决**：
1. 检查文件是否存在：
   ```bash
   ls ~/.claude/skills/videocut/智能划重点/SKILL.md
   ```
2. 检查 SKILL.md 格式是否正确（YAML front matter）
3. 重启 Claude Code

### Q3: "字幕太小"

**问题**：生成的字幕在视频中显示过小

**原因**：视频分辨率较低（如 720p）

**解决**：
编辑 `smart_highlight.py`，调整基础字号：
```python
Style: Default,PingFang SC,32,&H00FFFFFF,...  # 改为32pt
```

### Q4: "某些词不应该高亮"

**解决**：
编辑 `smart_highlight.py`，添加到禁用词：
```python
STOP_WORDS.add('你不想高亮的词')
```

或使用 `/videocut:自更新` 告诉 AI 你的偏好。

## 回滚到 V1.0

如果遇到问题需要回滚：

```bash
# 删除 V2.0
rm -rf ~/.claude/skills/videocut

# 恢复备份（如果你做了备份）
mv ~/.claude/skills/videocut.backup ~/.claude/skills/videocut

# 或重新安装 V1.0
git clone https://github.com/Ceeon/videocut-skills.git ~/.claude/skills/videocut
cd ~/.claude/skills/videocut
git checkout v1.0.0  # 切换到 V1.0 标签
```

## 反馈和支持

### 提供反馈

**方式1: Claude Code 内**
```
/videocut:自更新

告诉我：[你的反馈]
```

**方式2: GitHub Issues**
https://github.com/Ceeon/videocut-skills/issues

### 获取帮助

**文档**：
- 主文档：`README.md`
- 详细方法论：`智能划重点/tips/智能划重点方法论.md`
- 版本历史：`CHANGELOG.md`

**社区**：
- GitHub Discussions
- Issues 区

## 下一步

### 尝试新功能

1. 找一个已经剪辑好的视频
2. 在 Claude Code 中输入：
   ```
   /videocut:智能划重点
   ```
3. 查看生成的效果
4. 提供反馈帮助我们改进！

### 学习算法

如果你想了解"智能划重点"如何工作：

1. 阅读 `智能划重点/README.md` - 快速概览
2. 阅读 `智能划重点/tips/智能划重点方法论.md` - 详细算法
3. 阅读 `智能划重点/smart_highlight.py` - 源代码

### 定制化

智能划重点高度可定制：
- 关键词类别
- 优先级权重
- 高亮样式（颜色、大小）
- 每行高亮数量
- 禁用词列表

详见 `智能划重点/SKILL.md` 的配置部分。

---

**感谢升级到 V3.0！祝剪辑愉快！** 🎬✨
