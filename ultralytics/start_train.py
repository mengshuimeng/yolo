# run_yolo_training.py
import subprocess
import sys


def start_yolo_training():
    """
    启动YOLO模型训练
    """
    command = [
        'yolo',
        'task=detect',
        'mode=train',
        'data=D:\\Documents\\code\\python\\yolo\\datasets.yaml',
        'epochs=20',
        'batch=1',
        'model=D:\\Documents\\code\\python\\yolo\\runs\\detect\\train\\weights\\best.pt',
        'device=0',
        'imgsz=640',
        'workers=2'
    ]

    try:
        print("Executing command:", " ".join(command))
        # 执行命令并实时输出结果，使用UTF-8编码
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True,
            encoding='utf-8',
            errors='ignore'  # 忽略编码错误
        )

        # 实时打印输出
        for line in process.stdout:
            # 确保输出能正确显示
            print(line.strip(), flush=True)

        process.wait()

        if process.returncode == 0:
            print("Training completed successfully!")
        else:
            print("Training failed with return code:", process.returncode)

    except Exception as e:
        print("Training failed with exception:")
        print("Error:", str(e))


if __name__ == "__main__":
    # 设置控制台输出编码为UTF-8
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    start_yolo_training()
