"""
这份代码主要实现的功能是将一个文件夹里的图片按照输入的人数平均分配为多个文件夹

输入一个文件夹地址和一个人数变量
输出一个分配的文件夹，其包含多个子文件夹，每个子文件夹里有均分的照片，并且每个子文件夹的文件名为起始照片编号
"""

import os
import shutil
import argparse
from pathlib import Path


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='将文件夹中的图片按人数平均分配到多个子文件夹中')
    parser.add_argument('--source_folder', type=str, default='all_finall/all_finall', help='包含图片的源文件夹路径（默认：./images）')
    parser.add_argument('--num_people', type=int, default=30, help='分配的人数（默认：1）')
    parser.add_argument('--output_folder', type=str, default='distributed_images',
                        help='输出文件夹名称（默认：distributed_images）')

    return parser.parse_args()


def distribute_images(source_folder, num_people, output_folder="distributed_images"):
    """
    将图片按人数平均分配到不同的文件夹中

    Args:
        source_folder (str): 包含图片的源文件夹路径
        num_people (int): 分配的人数
        output_folder (str): 输出文件夹名称
    """
    # 获取源文件夹中的所有图片文件
    source_path = Path(source_folder)
    if not source_path.exists():
        raise FileNotFoundError(f"源文件夹不存在: {source_folder}")

    images = [f for f in source_path.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']]

    # 按文件名排序确保顺序一致
    images.sort()

    # 计算每个人应分配的图片数量
    total_images = len(images)
    if total_images == 0:
        print("源文件夹中没有找到图片文件")
        return

    images_per_person = total_images // num_people
    remaining_images = total_images % num_people

    # 创建输出文件夹
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)

    # 分配图片
    start_index = 0
    for person_id in range(num_people):
        # 计算当前人应获得的图片数量
        current_person_images = images_per_person + (1 if person_id < remaining_images else 0)
        end_index = start_index + current_person_images

        if current_person_images > 0:
            # 使用起始图片编号作为文件夹名称
            folder_name = str(start_index + 1)  # 从1开始编号
            person_folder = output_path / folder_name
            person_folder.mkdir(exist_ok=True)

            # 复制图片到对应文件夹
            for i in range(start_index, end_index):
                image_path = images[i]
                shutil.copy2(image_path, person_folder / image_path.name)

            print(f"已为第{person_id + 1}个人创建文件夹 {folder_name}，包含 {current_person_images} 张图片")

        start_index = end_index

    print(f"总共分配了 {total_images} 张图片给 {num_people} 个人")


def main():
    """主函数"""
    args = parse_args()
    distribute_images(args.source_folder, args.num_people, args.output_folder)


if __name__ == "__main__":
    main()
