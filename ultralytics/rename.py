import os
import shutil
from pathlib import Path
import argparse


def rename_and_merge_images(folder1_path, folder2_path, output_folder_path):
    """
    输入两个文件夹的路径
    每个文件夹都有很多张图片
    将这两个文件夹的每一张图片按照图片个数重命名 如1.jpg，2.jpg...保存到第三个文件夹下

    Args:
        folder1_path (str): 第一个图片文件夹路径
        folder2_path (str): 第二个图片文件夹路径
        output_folder_path (str): 输出文件夹路径
    """
    # 创建输出文件夹
    Path(output_folder_path).mkdir(parents=True, exist_ok=True)

    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # 先处理第一个文件夹
    count = 0
    for file in os.listdir(folder1_path):
        if Path(file).suffix.lower() in image_extensions:
            image_path = os.path.join(folder1_path, file)
            ext = Path(image_path).suffix
            count += 1
            new_filename = f"{count}{ext}"
            new_filepath = os.path.join(output_folder_path, new_filename)
            shutil.copy2(image_path, new_filepath)
            print(f"已复制第一个文件夹中的图片: {os.path.basename(image_path)} -> {new_filename}")

    # 再处理第二个文件夹
    for file in os.listdir(folder2_path):
        if Path(file).suffix.lower() in image_extensions:
            image_path = os.path.join(folder2_path, file)
            ext = Path(image_path).suffix
            count += 1
            new_filename = f"{count}{ext}"
            new_filepath = os.path.join(output_folder_path, new_filename)
            shutil.copy2(image_path, new_filepath)
            print(f"已复制第二个文件夹中的图片: {os.path.basename(image_path)} -> {new_filename}")

    print(f"总共处理了 {count} 张图片")


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="合并两个文件夹中的图片并按顺序重命名")
    parser.add_argument("-i1", "--input1", default="./finall", help="第一个输入图片文件夹路径 (默认: ./input1)")
    parser.add_argument("-i2", "--input2", default="./新建文件夹", help="第二个输入图片文件夹路径 (默认: ./input2)")
    parser.add_argument("-o", "--output", default="./1", help="输出图片文件夹路径 (默认: ./output)")
    return parser.parse_args()


if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()

    # 执行图片合并和重命名操作
    try:
        rename_and_merge_images(
            folder1_path=args.input1,
            folder2_path=args.input2,
            output_folder_path=args.output
        )
    except Exception as e:
        print(f"出错：{e}")
