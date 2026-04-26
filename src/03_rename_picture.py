"""
3. 将文件夹中的图片按顺序批量重命名为连续数字编号（如 1.jpg, 2.jpg, 3.jpg...）。
"""


import os
import shutil
from pathlib import Path
import argparse
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def natural_sort_key(text):
    """
    自然排序键函数，将字符串中的数字部分转换为整数进行比较
    例如: '1.jpg' < '10.jpg' < '100.jpg'
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def rename_images_in_folder(input_folder_path, output_folder_path, start_index=1):
    """
    将一个文件夹中的图片按照顺序重命名，比如0001.jpg、0002.jpg...

    Args:
        input_folder_path (str): 输入图片文件夹路径
        output_folder_path (str): 输出图片文件夹路径
        start_index (int): 起始编号，默认为1
    """
    input_path = resolve_project_path(input_folder_path)
    output_path = resolve_project_path(output_folder_path)

    if not input_path.exists():
        raise FileNotFoundError(f"输入图片文件夹不存在: {input_path}")
    if not input_path.is_dir():
        raise ValueError(f"输入路径不是文件夹: {input_path}")

    # 创建输出文件夹
    output_path.mkdir(parents=True, exist_ok=True)

    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # 获取文件夹中的所有图片文件
    images = []
    for file in os.listdir(input_path):
        if Path(file).suffix.lower() in image_extensions:
            images.append(file)

    # 使用自然排序对文件名进行排序
    images.sort(key=natural_sort_key)

    # 按顺序重命名并复制到输出文件夹
    # 按顺序重命名并复制到输出文件夹
    for index, filename in enumerate(images, start=start_index):
        # 获取原始文件扩展名
        # ext = Path(filename).suffix.lower()
        ext = '.jpg'
        # 创建新文件名
        new_filename = f"{index:04d}{ext}"
        old_filepath = input_path / filename
        new_filepath = output_path / new_filename
        if new_filepath.exists():
            raise FileExistsError(f"目标文件已存在，停止以避免覆盖: {new_filepath}")
        # 复制文件并重命名
        shutil.copy2(old_filepath, new_filepath)
        print(f"已复制：{filename} -> {new_filename}")


    print(f"总共处理了 {len(images)} 张图片")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="将一个文件夹中的图片按顺序重命名")
    parser.add_argument("-i", "--input", default=r"datasets_original\\20260426_dropzone1", help="输入图片文件夹路径（相对工程根目录）")
    parser.add_argument("-o", "--output", default=r"datasets_original\\20260426_dropzone2", help="输出图片文件夹路径（相对工程根目录）")
    parser.add_argument("-s", "--start", type=int, default=1, help="起始编号 (默认: 1)")
    return parser.parse_args()

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()

    # 执行图片重命名操作
    try:
        rename_images_in_folder(
            input_folder_path=args.input,
            output_folder_path=args.output,
            start_index=args.start
        )
    except Exception as e:
        print(f"出错：{e}")
