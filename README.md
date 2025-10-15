# 🎓 SayIt - AI智能语言学习平台

一个功能强大的AI驱动语言学习工具，集成视频字幕生成、智能笔记、强化学习和影子跟读功能。

## ✨ 核心功能

### 📹 智能字幕生成
- 🚀 **Faster-Whisper引擎**：采用优化的Whisper模型，提供词级精确时间戳
- 🤖 **LLM智能断句**：使用GPT-4o-mini智能恢复句末标点，支持转折词检测（so/but/because等）
- 📊 **质量验证**：自动拒绝异常断句结果（>30%标点率），智能回退到原始标点
- 🎯 **无字幕块处理**：自动识别静音片段，插入"[无字幕]"标记保持视频连贯性
- ⏱️ **微停顿优化**：智能合并<0.9s的自然人声停顿，避免过度分割

### 📝 AI学习笔记
- 🧠 **多维度解析**：单词、短语、语法、文化背景全方位学习
- 📖 **双格式输出**：支持Markdown和PDF格式
- 💾 **笔记管理**：本地存储，随时查看历史笔记
- 🎨 **精美排版**：专业的PDF布局设计

### 🎯 强化学习
- 📚 **词汇复习**：基于艾宾浩斯遗忘曲线的智能复习系统
- 🎲 **多种模式**：英译中、中译英、拼写练习
- 📊 **学习统计**：实时跟踪学习进度和正确率

### 🎬 影子跟读
- 🎥 **视频同步播放**：支持MP4视频播放
- 📜 **逐句字幕显示**：精确同步的字幕跟读
- ⏯️ **灵活控制**：暂停、重播、调整速度

### 🎵 QQ音乐支持
- 🎶 **歌词提取**：支持完整链接和短链接
- 📝 **歌词学习**：自动生成歌词学习笔记
- 🔗 **智能识别**：自动判断链接类型

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- FFmpeg（用于音视频处理）
- OpenAI API密钥（用于AI功能）

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
创建 `.env` 文件或设置环境变量：

```bash
# OpenAI API配置
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1  # 可选，自定义API端点

# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key"

# Linux/Mac
export OPENAI_API_KEY="your-api-key"
```

### 4. 启动应用

**Windows**（推荐）：
```powershell
.\启动应用.ps1
```

**手动启动**：
```bash
python run.py
```

### 5. 访问应用
打开浏览器访问：`http://localhost:5000`

## 💡 使用指南

### 📹 生成字幕笔记
1. 在"笔记生成"标签页粘贴视频链接（YouTube、Bilibili等）
2. 系统自动下载视频/音频
3. 使用Faster-Whisper提取语音并生成精确字幕
4. LLM智能断句和标点恢复
5. 生成AI学习笔记（Markdown/PDF）

### 📚 查看笔记
- 在"笔记存储"标签页浏览所有历史笔记
- 支持Markdown预览和PDF下载

### 🎯 强化学习
- 选择已保存的笔记进入学习模式
- 多种题型随机出题
- 实时反馈和统计

### 🎬 影子跟读
- 选择已下载的视频
- 同步播放视频和字幕
- 跟读练习，提升口语

## 🎯 支持的平台

### 视频平台
- ✅ YouTube
- ✅ Bilibili
- ✅ TikTok/抖音
- ✅ Vimeo
- ✅ 其他主流视频平台

### 音乐平台
- ✅ QQ音乐（完整链接和短链接）

## 📦 技术栈

### 后端
- **Flask** - Web框架
- **faster-whisper** - 优化的语音识别引擎
- **OpenAI GPT-4o-mini** - AI笔记生成和智能断句
- **yt-dlp** - 视频/音频下载
- **ReportLab** - PDF生成

### 前端
- **原生JavaScript** - 交互逻辑
- **响应式CSS** - 现代化UI设计
- **Bootstrap** - 界面组件

## 🔧 核心技术亮点

### 1️⃣ Faster-Whisper集成
```python
# 词级时间戳
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    audio_path,
    word_timestamps=True,
    vad_filter=True
)
```

### 2️⃣ LLM智能标点恢复
```python
# 只对10-20%的词添加标点
# 支持转折词检测（so/but/because等）
# 自动验证输出质量（>30%拒绝）
punct_tokens = restore_sentence_final_punct_by_llm(tokens)
```

### 3️⃣ 微停顿处理
```python
# 合并<0.9s的自然停顿
MICRO_GAP_THRESHOLD = 0.9
if gap_duration < MICRO_GAP_THRESHOLD:
    extend_previous_segment(gap_duration)
```

## 📊 项目结构

```
V0_SayIt/
├── app/
│   ├── routes/          # 路由模块
│   │   ├── main.py      # 主页路由
│   │   ├── generation.py # 笔记生成
│   │   ├── notes.py     # 笔记管理
│   │   ├── learning.py  # 强化学习
│   │   └── shadowing.py # 影子跟读
│   ├── services/        # 业务逻辑
│   │   ├── video_service.py
│   │   ├── note_service.py
│   │   └── ai_service.py
│   └── utils/           # 工具函数
│       ├── caption.py   # 字幕生成（Faster-Whisper）
│       ├── ai.py        # AI功能（LLM标点恢复）
│       ├── audio.py     # 音视频下载
│       ├── pdf.py       # PDF生成
│       └── music.py     # QQ音乐
├── templates/           # HTML模板
├── static/             # 静态资源
├── videos/             # 视频/音频存储
├── captions/           # 字幕文件
├── notes/              # 笔记存储
├── pdfs/               # PDF输出
└── requirements.txt    # 依赖列表
```

## 🎉 特色亮点

- ✅ **词级精确时间戳**：Faster-Whisper提供毫秒级准确度
- ✅ **AI智能断句**：LLM根据语义和转折词智能断句
- ✅ **质量自动验证**：拒绝过度断句，确保输出质量
- ✅ **完整学习闭环**：观看→记录→学习→跟读
- ✅ **多平台支持**：YouTube、B站、抖音等
- ✅ **无字幕块处理**：保持视频连贯性
- ✅ **微停顿优化**：自然的句子分割
- ✅ **中文完美支持**：全中文界面和文档

## ⚙️ 配置说明

### Whisper模型选择
在 `app/utils/caption.py` 中可调整模型大小：
```python
# 可选: tiny, base, small, medium, large-v2, large-v3
model = WhisperModel("small", device="cpu", compute_type="int8")
```

### LLM标点恢复
- 阈值：拒绝>30%标点率的异常结果
- 微停顿：<0.9s的停顿会被合并
- 转折词：so/but/because/however等

### 环境变量
```bash
OPENAI_API_KEY=sk-xxx           # 必需
OPENAI_BASE_URL=https://...     # 可选
```

## 📖 详细文档

- [影子跟读功能说明.md](./影子跟读功能说明.md)
- [字幕质量优化指南.md](./字幕质量优化指南.md)
- [最新优化总结.md](./最新优化总结.md)

## ⚠️ 注意事项

- 首次运行会下载Faster-Whisper模型（约150MB）
- PDF生成和LLM功能需要配置OpenAI API密钥
- 视频下载速度取决于网络环境
- 部分视频可能因版权或地区限制无法下载

## 🔄 版本历史

### v2.0.0 (当前版本)
- ✨ 集成Faster-Whisper，提供词级时间戳
- ✨ LLM智能标点恢复和断句
- ✨ 输出质量自动验证机制
- ✨ 无字幕块和微停顿优化
- ✨ 恢复影子跟读功能
- 🐛 修复视频下载后台任务

### v1.0.0
- 基础字幕生成功能
- AI笔记生成
- 强化学习模块
- QQ音乐支持

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 开源协议

MIT License

---

**开发者**: uzzz0119  
**AI模型**: OpenAI GPT-4o-mini + Faster-Whisper  
**界面**: 响应式Web设计  
**GitHub**: https://github.com/uzzz0119/SayIt

**⭐ 如果这个项目对你有帮助，请给个Star！**
