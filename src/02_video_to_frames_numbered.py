"""
2. 将视频文件拆分成连续的图片帧，并按数字顺序命名保存。
def parse_args():修改参数
"""


#!/usr/bin/env python3
import cv2
import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(path_str: str) -> str:
    path = Path(path_str)
    if path.is_absolute():
        return str(path)
    return str((PROJECT_ROOT / path).resolve())


def video_to_frames_numbered(
    video_path: str,
    out_dir: str,
    img_ext: str = "jpg",
    step: int = 1,
    start_index: int = 1,
):
    video_path = Path(resolve_project_path(video_path))
    out_dir = Path(resolve_project_path(out_dir))
    if step < 1:
        raise ValueError("step 必须 >= 1")
    if start_index < 1:
        raise ValueError("start_index 必须 >= 1")
    if not video_path.exists():
        raise FileNotFoundError(f"找不到视频文件: {video_path}")
    if not video_path.is_file():
        raise ValueError(f"输入路径不是文件: {video_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频文件: {video_path}")

    frame_idx = 0
    saved_count = 0
    out_index = start_index

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_idx % step == 0:
                filename = f"{out_index:04d}.{img_ext}"
                out_path = out_dir / filename
                if out_path.exists():
                    raise FileExistsError(f"目标文件已存在，停止以避免覆盖: {out_path}")

                success = cv2.imwrite(str(out_path), frame)
                if not success:
                    print(f"警告：写入失败 -> {out_path}")
                else:
                    saved_count += 1
                    out_index += 1
                    if saved_count % 100 == 0:
                        print(f"已保存 {saved_count} 张图片...")
            frame_idx += 1
    finally:
        cap.release()

    print(f"完成：总共保存 {saved_count} 张图片 到 {out_dir}")

def parse_args():
    p = argparse.ArgumentParser(description="将视频拆成图片并按 1,2,3... 命名。")
    p.add_argument("-i", "--input", default=r"videos\video_20260426_181953.mp4", help="输入视频文件路径 ")
    p.add_argument("-o", "--output", default=r"datasets_original\20260426_dropzone1", help="输出图片文件夹 (默认: ./frames)")
    p.add_argument("-f", "--format", default="jpg", choices=["jpg", "png", "bmp"], help="输出图片格式 (默认: jpg)")
    p.add_argument("--step", type=int, default=3, help="抽帧步长（默认 3，表示每隔 3 帧保存 1 张）")
    p.add_argument("--start", type=int, default=1032, help="输出序号起始值（默认 1032）")
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
