# grasp_inference.py
import cv2
from ultralytics import YOLO
import os


def run_inference(image_path, model_path='grasp_detector.pt', save_results=True):
    """
    使用 grasp_detector.pt 模型进行推理

    参数:
        image_path: 图片路径或图片文件夹路径
        model_path: 模型权重文件路径
        save_results: 是否保存结果图片
    """

    # 加载模型
    print(f"正在加载模型：{model_path}")
    model = YOLO(model_path)
    print("模型加载完成！")

    # 获取模型信息
    info = model.info()
    print(f"\n模型信息：{info}")

    # 判断是单张图片还是文件夹
    if os.path.isfile(image_path):
        # 单张图片推理
        print(f"\n正在推理图片：{image_path}")
        results = model.predict(source=image_path, save=save_results)

        # 显示结果
        for result in results:
            boxes = result.boxes
            if len(boxes) > 0:
                print(f"\n检测到 {len(boxes)} 个目标:")
                for i, box in enumerate(boxes):
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    xyxy = box.xyxy[0].tolist()
                    print(f"  目标 {i+1}: 类别={cls}, 置信度={conf:.2f}, 坐标={xyxy}")
            else:
                print("\n未检测到任何目标")

            # 如果保存了结果，显示保存路径
            if save_results and hasattr(result, 'save_dir'):
                print(f"\n结果已保存到：{result.save_dir}")

    elif os.path.isdir(image_path):
        # 文件夹批量推理
        print(f"\n正在批量推理文件夹：{image_path}")
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']

        image_files = []
        for file in os.listdir(image_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(image_path, file))

        if not image_files:
            print(f"在文件夹中未找到图片文件")
            return

        print(f"找到 {len(image_files)} 张图片")

        # 批量推理
        results = model.predict(source=image_path, save=save_results)

        # 统计结果
        total_detections = 0
        for result in results:
            boxes = result.boxes
            total_detections += len(boxes)

        print(f"\n推理完成！")
        print(f"总共检测图片数：{len(image_files)}")
        print(f"总共检测到目标数：{total_detections}")
        if save_results:
            print(f"结果图片保存在：runs/detect/predict/")

    else:
        print(f"错误：找不到文件或文件夹 '{image_path}'")


# ... existing code ...
if __name__ == "__main__":
    import sys

    # 默认配置
    default_model = 'D:\\Documents\\code\\python\\yolo\\grasp_detector.pt'

    # 检查命令行参数
    if len(sys.argv) > 1:
        image_source = sys.argv[1]
    else:
        # 如果没有提供参数，提示用户输入
        print("=" * 60)
        print("Grasp Detector - YOLO 推理工具")
        print("=" * 60)
        print("\n用法:")
        print("  1. 直接运行：python grasp_inference.py")
        print("     然后输入图片路径或文件夹路径")
        print("\n  2. 命令行运行：python grasp_inference.py <图片路径/文件夹路径>")
        print("\n示例:")
        print("  python grasp_inference.py D:/images/test.jpg")
        print("  python grasp_inference.py D:/images/test_folder/")
        print("=" * 60)
        print()

        # 使用 sys.stdin.readline 避免 input() 的显示问题
        import io
        sys.stdout.flush()
        print("请输入要推理的图片路径或文件夹路径：", end='', flush=True)
        image_source = sys.stdin.readline().strip()

    if image_source:
        run_inference(image_source, model_path=default_model)
    else:
        print("未提供图片路径，程序退出。")
# ... existing code ...

