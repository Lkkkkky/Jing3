'''
=========================================================
@File     : dy.py
@IDE      : PyCharm
@Author   : Jing3
@Date     : 2025/1/20
@Desc     : 抖音视频去重处理工具 - 通过多种技术手段处理视频以避免平台重复检测
=========================================================
'''

import cv2
import numpy as np
import os
import random
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
import argparse
from pathlib import Path

class VideoProcessor:
    def __init__(self):
        self.output_dir = "processed_videos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def add_invisible_watermark(self, video_path, output_path):
        """添加不可见水印 - 在视频中添加微弱的噪点"""
        print("正在添加不可见水印...")
        
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 添加随机噪点（强度很低，肉眼几乎不可见）
            noise = np.random.randint(-2, 3, frame.shape, dtype=np.int16)
            frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            
            # 每隔一定帧数添加更细微的变化
            if frame_count % 30 == 0:
                # 轻微调整亮度
                brightness_adjust = random.randint(-3, 3)
                frame = np.clip(frame.astype(np.int16) + brightness_adjust, 0, 255).astype(np.uint8)
            
            out.write(frame)
            frame_count += 1
        
        cap.release()
        out.release()
        print(f"不可见水印添加完成: {output_path}")
    
    def adjust_video_properties(self, video_path, output_path):
        """调整视频属性 - 微调帧率、分辨率等"""
        print("正在调整视频属性...")
        
        clip = VideoFileClip(video_path)
        
        # 微调帧率（±0.1fps）
        fps_adjustment = random.uniform(-0.1, 0.1)
        new_fps = max(1, clip.fps + fps_adjustment)
        
        # 微调分辨率（缩放比例在0.998-1.002之间）
        scale_factor = random.uniform(0.998, 1.002)
        new_width = int(clip.w * scale_factor)
        new_height = int(clip.h * scale_factor)
        
        # 确保宽高是偶数（视频编码要求）
        new_width = new_width if new_width % 2 == 0 else new_width + 1
        new_height = new_height if new_height % 2 == 0 else new_height + 1
        
        # 应用调整
        processed_clip = clip.resize((new_width, new_height)).set_fps(new_fps)
        
        # 写入文件
        processed_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        clip.close()
        processed_clip.close()
        print(f"视频属性调整完成: {output_path}")
    
    def add_transparent_overlay(self, video_path, output_path):
        """添加透明覆盖层 - 在视频上添加极其透明的色彩层"""
        print("正在添加透明覆盖层...")
        
        clip = VideoFileClip(video_path)
        
        # 创建一个极其透明的彩色覆盖层
        overlay_colors = [
            (255, 0, 0),    # 红色
            (0, 255, 0),    # 绿色
            (0, 0, 255),    # 蓝色
            (255, 255, 0),  # 黄色
            (255, 0, 255),  # 紫色
        ]
        
        color = random.choice(overlay_colors)
        
        # 创建透明度极低的覆盖层（透明度0.005-0.01）
        opacity = random.uniform(0.005, 0.01)
        overlay = ColorClip(
            size=(clip.w, clip.h),
            color=color,
            duration=clip.duration
        ).set_opacity(opacity)
        
        # 合成视频
        final_clip = CompositeVideoClip([clip, overlay])
        
        # 写入文件
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        clip.close()
        overlay.close()
        final_clip.close()
        print(f"透明覆盖层添加完成: {output_path}")
    
    def modify_metadata(self, video_path, output_path):
        """修改视频元数据"""
        print("正在修改视频元数据...")
        
        clip = VideoFileClip(video_path)
        
        # 生成随机的编码参数来改变文件特征
        crf_value = random.randint(18, 23)  # 质量参数
        preset = random.choice(['medium', 'slow', 'fast'])
        
        # 写入文件时使用不同的编码参数
        clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            ffmpeg_params=[
                '-crf', str(crf_value),
                '-preset', preset,
                '-movflags', '+faststart'
            ],
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        clip.close()
        print(f"视频元数据修改完成: {output_path}")
    
    def process_video(self, input_path, methods=['watermark', 'properties', 'overlay', 'metadata']):
        """处理视频的主函数"""
        if not os.path.exists(input_path):
            print(f"错误: 输入文件不存在 - {input_path}")
            return None
        
        input_filename = Path(input_path).stem
        input_extension = Path(input_path).suffix
        
        current_path = input_path
        
        # 按顺序应用各种处理方法
        for i, method in enumerate(methods):
            temp_output = os.path.join(
                self.output_dir, 
                f"{input_filename}_step{i+1}_{method}{input_extension}"
            )
            
            try:
                if method == 'watermark':
                    self.add_invisible_watermark(current_path, temp_output)
                elif method == 'properties':
                    self.adjust_video_properties(current_path, temp_output)
                elif method == 'overlay':
                    self.add_transparent_overlay(current_path, temp_output)
                elif method == 'metadata':
                    self.modify_metadata(current_path, temp_output)
                
                # 删除中间文件（除了第一个输入文件）
                if current_path != input_path and os.path.exists(current_path):
                    os.remove(current_path)
                
                current_path = temp_output
                
            except Exception as e:
                print(f"处理方法 {method} 时出错: {str(e)}")
                continue
        
        # 重命名最终文件
        final_output = os.path.join(
            self.output_dir,
            f"{input_filename}_processed{input_extension}"
        )
        
        if os.path.exists(current_path):
            os.rename(current_path, final_output)
            print(f"\n✅ 视频处理完成!")
            print(f"原文件: {input_path}")
            print(f"处理后: {final_output}")
            print(f"应用的处理方法: {', '.join(methods)}")
            return final_output
        
        return None
    
    def batch_process(self, input_dir, file_extensions=['.mp4', '.avi', '.mov', '.mkv']):
        """批量处理目录中的视频文件"""
        if not os.path.exists(input_dir):
            print(f"错误: 输入目录不存在 - {input_dir}")
            return
        
        video_files = []
        for ext in file_extensions:
            video_files.extend(Path(input_dir).glob(f"*{ext}"))
            video_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
        
        if not video_files:
            print(f"在目录 {input_dir} 中未找到视频文件")
            return
        
        print(f"找到 {len(video_files)} 个视频文件，开始批量处理...")
        
        processed_count = 0
        for video_file in video_files:
            print(f"\n处理文件 {processed_count + 1}/{len(video_files)}: {video_file.name}")
            result = self.process_video(str(video_file))
            if result:
                processed_count += 1
        
        print(f"\n批量处理完成! 成功处理 {processed_count}/{len(video_files)} 个文件")

def main():
    parser = argparse.ArgumentParser(description='抖音视频去重处理工具')
    parser.add_argument('input', help='输入视频文件路径或目录路径')
    parser.add_argument('--methods', nargs='+', 
                       choices=['watermark', 'properties', 'overlay', 'metadata'],
                       default=['watermark', 'properties', 'overlay', 'metadata'],
                       help='选择处理方法')
    parser.add_argument('--batch', action='store_true', help='批量处理模式')
    
    args = parser.parse_args()
    
    processor = VideoProcessor()
    
    print("🎬 抖音视频去重处理工具")
    print("=" * 50)
    print("功能说明:")
    print("1. 添加不可见水印 - 在视频中加入微弱噪点")
    print("2. 调整视频属性 - 微调帧率和分辨率")
    print("3. 添加透明覆盖层 - 加入极其透明的色彩层")
    print("4. 修改视频元数据 - 改变编码参数")
    print("=" * 50)
    
    if args.batch:
        processor.batch_process(args.input)
    else:
        processor.process_video(args.input, args.methods)

if __name__ == "__main__":
    # 如果没有命令行参数，提供交互式界面
    import sys
    if len(sys.argv) == 1:
        print("🎬 抖音视频去重处理工具")
        print("=" * 50)
        
        input_path = input("请输入视频文件路径: ").strip('"')
        
        if not input_path:
            print("错误: 请提供有效的文件路径")
            sys.exit(1)
        
        print("\n可用的处理方法:")
        print("1. watermark - 添加不可见水印")
        print("2. properties - 调整视频属性")
        print("3. overlay - 添加透明覆盖层")
        print("4. metadata - 修改视频元数据")
        
        method_choice = input("\n选择处理方法 (输入数字，多个用空格分隔，回车使用全部): ").strip()
        
        if method_choice:
            method_map = {
                '1': 'watermark',
                '2': 'properties', 
                '3': 'overlay',
                '4': 'metadata'
            }
            methods = [method_map.get(m.strip()) for m in method_choice.split() if m.strip() in method_map]
            if not methods:
                methods = ['watermark', 'properties', 'overlay', 'metadata']
        else:
            methods = ['watermark', 'properties', 'overlay', 'metadata']
        
        processor = VideoProcessor()
        processor.process_video(input_path, methods)
    else:
        main()