"""
我现在有一个文件夹，文件夹名为lib

这个文件夹里有很多`数字.txt`文件，只有一个是`classes.txt`文件

我现在想要将每一个`数字.txt`文件中的每一行的第一个数字替换掉，`classes.txt`文件不要替换
例如他原来是的第一行是数字1 但是现在要修改为数字0

输入文件夹地址
输入原来的数字
输入修改的数字
输出将txt修改并输出另一个目录
"""

import os
import shutil

def process_txt_files(source_folder, target_folder, old_number, new_number):
    """
    Process all txt files in source folder, replace first number in each line
    and save to target folder.

    Args:
        source_folder (str): Path to source folder containing txt files
        target_folder (str): Path to target folder for output files
        old_number (str): Original number to be replaced
        new_number (str): New number to replace with
    """
    # Create target folder if not exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Process each file in source folder
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)

        # Skip classes.txt and non-txt files
        if filename == 'classes.txt' or not filename.endswith('.txt'):
            # Copy classes.txt directly to target folder
            if filename == 'classes.txt':
                target_path = os.path.join(target_folder, filename)
                shutil.copy2(source_path, target_path)
            continue

        # Process txt files
        target_path = os.path.join(target_folder, filename)
        process_single_file(source_path, target_path, old_number, new_number)

def process_single_file(source_path, target_path, old_number, new_number):
    """
    Process a single txt file, replace first number in each line.

    Args:
        source_path (str): Path to source file
        target_path (str): Path to target file
        old_number (str): Original number to be replaced
        new_number (str): New number to replace with
    """
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process each line
    processed_lines = []
    for line in lines:
        # Split line into parts
        parts = line.strip().split()
        if parts:
            # Replace first part if it matches old_number
            if parts[0] == old_number:
                parts[0] = new_number
            processed_lines.append(' '.join(parts) + '\n')
        else:
            processed_lines.append(line)

    # Write processed lines to target file
    with open(target_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

def main():
    """Main function to get user input and process files."""
    # Get user inputs
    source_folder = input("请输入源文件夹地址: ").strip()
    old_number = input("请输入要替换的原数字: ").strip()
    new_number = input("请输入替换后的数字: ").strip()

    # Generate target folder name
    source_parent = os.path.dirname(source_folder)
    source_name = os.path.basename(source_folder)
    target_folder = os.path.join(source_parent, f"{source_name}_processed")

    # Process files
    process_txt_files(source_folder, target_folder, old_number, new_number)
    print(f"处理完成！结果已保存至: {target_folder}")

if __name__ == "__main__":
    main()
