# 抖音视频去重处理工具

这是一个专门用于处理视频以避免抖音平台重复检测的工具。通过多种技术手段对视频进行微调，在不改变原有内容和时长的前提下，让视频在平台算法看来是"新"的内容。

## 功能特性

### 🔧 处理方法

1. **不可见水印** (`watermark`)
   - 在视频中添加微弱的随机噪点
   - 肉眼几乎不可见，但能改变视频的数字指纹
   - 每30帧进行轻微亮度调整

2. **视频属性调整** (`properties`)
   - 微调帧率（±0.1fps）
   - 微调分辨率（缩放比例0.998-1.002）
   - 保持视频质量的同时改变技术参数

3. **透明覆盖层** (`overlay`)
   - 添加极其透明的彩色覆盖层（透明度0.005-0.01）
   - 随机选择颜色，视觉上几乎无感知
   - 有效改变视频的像素特征

4. **元数据修改** (`metadata`)
   - 使用不同的编码参数重新编码
   - 随机调整CRF质量参数（18-23）
   - 改变编码预设（medium/slow/fast）

## 安装依赖

```bash
pip install -r requirements.txt
```

### 系统要求

- Python 3.7+
- FFmpeg（MoviePy依赖）

#### Windows安装FFmpeg
1. 下载FFmpeg: https://ffmpeg.org/download.html
2. 解压到任意目录
3. 将FFmpeg的bin目录添加到系统PATH环境变量

#### macOS安装FFmpeg
```bash
brew install ffmpeg
```

#### Linux安装FFmpeg
```bash
sudo apt update
sudo apt install ffmpeg
```

## 使用方法

### 1. 交互式模式（推荐新手）

直接运行脚本，按提示操作：

```bash
python dy.py
```

### 2. 命令行模式

#### 处理单个视频文件

```bash
# 使用所有处理方法
python dy.py "path/to/your/video.mp4"

# 只使用特定方法
python dy.py "path/to/your/video.mp4" --methods watermark properties
```

#### 批量处理目录中的视频

```bash
# 批量处理目录中的所有视频文件
python dy.py "path/to/video/directory" --batch

# 批量处理并指定处理方法
python dy.py "path/to/video/directory" --batch --methods overlay metadata
```

### 3. 参数说明

- `input`: 输入视频文件路径或目录路径
- `--methods`: 选择处理方法，可选值：
  - `watermark`: 添加不可见水印
  - `properties`: 调整视频属性
  - `overlay`: 添加透明覆盖层
  - `metadata`: 修改视频元数据
- `--batch`: 启用批量处理模式

## 使用示例

### 示例1：处理单个视频

```bash
python dy.py "C:\Videos\original.mp4"
```

输出文件将保存在 `processed_videos/original_processed.mp4`

### 示例2：只使用水印和属性调整

```bash
python dy.py "video.mp4" --methods watermark properties
```

### 示例3：批量处理整个文件夹

```bash
python dy.py "C:\Videos" --batch
```

## 输出说明

- 处理后的视频保存在 `processed_videos` 目录中
- 文件命名格式：`原文件名_processed.扩展名`
- 支持的视频格式：MP4, AVI, MOV, MKV

## 技术原理

### 为什么这些方法有效？

1. **数字指纹改变**：通过添加噪点和微调参数，改变视频的MD5哈希值
2. **像素级差异**：透明覆盖层在像素级别创造差异
3. **编码特征变化**：不同的编码参数产生不同的文件特征
4. **元数据差异**：编码时间戳和参数的变化

### 质量保证

- 所有处理都在视觉无感知的范围内
- 保持原始视频的时长和主要内容
- 质量损失控制在最小范围

## 注意事项

⚠️ **重要提醒**

1. **合规使用**：请确保您的视频内容符合平台规定
2. **原创保护**：本工具不应用于侵犯他人版权的内容
3. **适度使用**：过度依赖技术手段可能影响内容质量
4. **备份原文件**：处理前请备份原始视频文件

## 常见问题

### Q: 处理后的视频质量会下降吗？
A: 质量损失极小，肉眼几乎无法察觉。所有调整都在视觉无感知范围内。

### Q: 支持哪些视频格式？
A: 支持MP4、AVI、MOV、MKV等常见格式，推荐使用MP4格式。

### Q: 处理时间需要多久？
A: 处理时间取决于视频大小和选择的方法，通常为原视频时长的1-3倍。

### Q: 可以重复处理同一个视频吗？
A: 可以，但建议适度使用，避免过度处理影响质量。

## 更新日志

### v1.0.0
- 初始版本发布
- 支持四种核心处理方法
- 提供交互式和命令行两种使用模式
- 支持批量处理功能

## 技术支持

如果遇到问题或有改进建议，请联系开发者。

---

**免责声明**：本工具仅供学习和研究使用，使用者需自行承担使用风险，并确保遵守相关平台的服务条款。