#!/usr/bin/env python3
import cv2
import os
import argparse

def video_to_frames_numbered(video_path: str, out_dir: str, img_ext: str = "jpg", step: int = 1, start_index: int = 1):
    if step < 1:
        raise ValueError("step 必须 >= 1")
    if start_index < 1:
        raise ValueError("start_index 必须 >= 1")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"找不到视频文件: {video_path}")
    os.makedirs(out_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频文件: {video_path}")

    frame_idx = 0
    saved_count = 0
    out_index = start_index

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % step == 0:
            filename = f"{out_index}.{img_ext}"
            out_path = os.path.join(out_dir, filename)
            success = cv2.imwrite(out_path, frame)
            if not success:
                print(f"警告：写入失败 -> {out_path}")
            else:
                saved_count += 1
                out_index += 1
                if saved_count % 100 == 0:
                    print(f"已保存 {saved_count} 张图片...")
        frame_idx += 1

    cap.release()
    print(f"完成：总共保存 {saved_count} 张图片 到 {out_dir}")

def parse_args():
    p = argparse.ArgumentParser(description="将视频拆成图片并按 1,2,3... 命名。")
    p.add_argument("-i", "--input", default="7.mp4", help="输入视频文件路径 ")
    p.add_argument("-o", "--output", default="./output", help="输出图片文件夹 (默认: ./frames)")
    p.add_argument("-f", "--format", default="jpg", choices=["jpg", "png", "bmp"], help="输出图片格式 (默认: jpg)")
    p.add_argument("--step", type=int, default=1, help="抽帧步长（默认1，表示每帧保存）")
    p.add_argument("--start", type=int, default=7302, help="输出序号起始值，默认1")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        video_to_frames_numbered(
            video_path=args.input,
            out_dir=args.output,
            img_ext=args.format,
            step=args.step,
            start_index=args.start
        )
    except Exception as e:
        print("出错：", e)
