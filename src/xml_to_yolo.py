"""
批量转换 XML 标注为 YOLO 格式
"""

import os
import xml_to_yolo.etree.ElementTree as ET

# 👇 请根据你的数据集修改这个字典！
# class_name → class_id（从0开始）
CLASS_MAPPING = {
    "cat": 0,
    "dog": 1,
    # 添加你自己的类别，例如：
    # "person": 0,
    # "car": 1,
    # "bicycle": 2,
}

def convert_xml_to_yolo_txt(xml_path, txt_path, class_mapping):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 获取图像尺寸
    size = root.find("size")
    if size is None:
        raise ValueError(f"Missing <size> in {xml_path}")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    lines = []
    for obj in root.findall("object"):
        name = obj.find("name").text.strip()
        if name not in class_mapping:
            print(f"Warning: Unknown class '{name}' in {xml_path}, skipped.")
            continue

        class_id = class_mapping[name]

        bndbox = obj.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)

        # 转换为 YOLO 格式
        x_center = (xmin + xmax) / 2.0 / width
        y_center = (ymin + ymax) / 2.0 / height
        box_width = (xmax - xmin) / width
        box_height = (ymax - ymin) / height

        # 确保数值在 [0, 1] 范围内（防止标注越界）
        x_center = max(0.0, min(1.0, x_center))
        y_center = max(0.0, min(1.0, y_center))
        box_width = max(0.0, min(1.0, box_width))
        box_height = max(0.0, min(1.0, box_height))

        lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}")

    # 写入 .txt 文件（即使没有对象也创建空文件）
    with open(txt_path, "w") as f:
        f.write("\n".join(lines))

def batch_convert(xml_dir, output_dir, class_mapping):
    os.makedirs(output_dir, exist_ok=True)
    xml_files = [f for f in os.listdir(xml_dir) if f.endswith(".xml")]

    for xml_file in xml_files:
        xml_path = os.path.join(xml_dir, xml_file)
        txt_file = xml_file.replace(".xml", ".txt")
        txt_path = os.path.join(output_dir, txt_file)
        try:
            convert_xml_to_yolo_txt(xml_path, txt_path, class_mapping)
        except Exception as e:
            print(f"Error processing {xml_path}: {e}")

# ========================
# 🚀 使用示例
# ========================
if __name__ == "__main__":
    XML_DIR = "D:\Desktop\\temp\labels"          # 替换为你的 .xml 文件夹路径
    OUTPUT_TXT_DIR = "D:\Desktop\\temp\\1" # 输出 .txt 文件夹

    # ⚠️ 务必修改 CLASS_MAPPING 为你自己的类别！
    CLASS_MAPPING = {
        "0": 0
    }

    batch_convert(XML_DIR, OUTPUT_TXT_DIR, CLASS_MAPPING)
    print("✅ 转换完成！")
