# 🎬 智能字幕 & 歌词笔记生成器

一个智能的学习工具，支持视频字幕提取和QQ音乐歌词学习，自动生成AI学习笔记。

## ✨ 核心功能

- 🧠 **智能识别**：自动判断视频链接或QQ音乐链接
- 📹 **视频字幕**：支持YouTube、Bilibili等主流平台
- 🎵 **QQ音乐**：支持完整链接和短链接
- 🤖 **AI笔记**：使用GPT生成结构化学习笔记
- 📝 **双格式**：支持TXT文本和PDF笔记输出

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key"

# Linux/Mac
export OPENAI_API_KEY="your-api-key"
```

### 3. 启动应用
```bash
python app.py
```

### 4. 打开浏览器
访问 `http://localhost:5000`

## 💡 使用方法

1. **粘贴链接**：在输入框中粘贴视频或QQ音乐链接
2. **自动识别**：系统会实时显示识别的链接类型
3. **选择格式**：点击按钮选择文本或PDF格式
4. **下载文件**：处理完成后自动下载

## 🎯 支持的链接

### 视频平台
- YouTube
- Bilibili
- Vimeo
- 其他主流视频平台

### QQ音乐
- 完整链接：`https://y.qq.com/n/ryqq/songDetail/xxxxx`
- 短链接：`https://c6.y.qq.com/base/fcgi-bin/u?__=xxxxx`

## 📦 依赖包

- Flask - Web框架
- yt-dlp - 视频下载
- openai-whisper - 语音识别
- openai - AI笔记生成
- reportlab - PDF生成
- requests - HTTP请求

## 📖 详细文档

查看 [QQ音乐功能说明.md](./QQ音乐功能说明.md) 了解更多详细信息。

## 🎉 特色亮点

- ✅ 单一输入框，简洁易用
- ✅ 实时链接类型识别
- ✅ 彩色视觉反馈
- ✅ 智能短链接解析
- ✅ 自动临时文件清理
- ✅ 完美中文支持

## ⚠️ 注意事项

- PDF笔记生成需要配置OpenAI API密钥
- 部分歌曲可能因版权限制无法获取
- 建议使用稳定的网络连接

## 📝 示例

```
# 视频字幕
输入：https://www.youtube.com/watch?v=xxxxx
输出：视频字幕学习笔记.pdf

# QQ音乐歌词
输入：https://c6.y.qq.com/base/fcgi-bin/u?__=xxxxx
输出：歌曲名_歌词笔记.pdf
```

---

**开发语言**: Python + JavaScript  
**AI模型**: OpenAI GPT-4o-mini  
**界面**: 响应式Web设计

