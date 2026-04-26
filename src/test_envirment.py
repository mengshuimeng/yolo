import importlib
import platform
import sys
from typing import Any


MODULES_TO_CHECK = [
    "cv2",
    "numpy",
    "torch",
    "torchvision",
    "ultralytics",
]


def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def format_value(value: Any) -> str:
    return "None" if value is None else str(value)


def check_python_environment() -> None:
    print_header("1. Python 环境")
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"Python 可执行文件: {sys.executable}")
    print(f"平台信息: {platform.platform()}")
    print(f"系统架构: {platform.machine()}")


def check_modules() -> dict[str, Any]:
    print_header("2. 依赖模块检查")
    imported_modules: dict[str, Any] = {}

    for module_name in MODULES_TO_CHECK:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "未知版本")
            imported_modules[module_name] = module
            print(f"[OK] {module_name:<12} 已安装，版本: {version}")
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[FAIL] {module_name:<12} 导入失败: {exc}")

    return imported_modules


def check_gpu(imported_modules: dict[str, Any]) -> None:
    print_header("3. GPU / CUDA 检查")

    torch = imported_modules.get("torch")
    if torch is None:
        print("未检测到 torch，无法继续检查 GPU。")
        return

    print(f"PyTorch 版本: {format_value(getattr(torch, '__version__', None))}")
    print(f"PyTorch CUDA 版本: {format_value(getattr(torch.version, 'cuda', None))}")
    print(f"cuDNN 可用: {torch.backends.cudnn.is_available()}")
    print(f"cuDNN 版本: {format_value(torch.backends.cudnn.version())}")
    print(f"CUDA 是否可用: {torch.cuda.is_available()}")

    if not torch.cuda.is_available():
        print("当前未检测到可用 GPU，训练和推理将默认使用 CPU。")
        return

    gpu_count = torch.cuda.device_count()
    current_device = torch.cuda.current_device()
    print(f"GPU 数量: {gpu_count}")
    print(f"当前设备索引: {current_device}")

    for index in range(gpu_count):
        props = torch.cuda.get_device_properties(index)
        total_memory_gb = props.total_memory / (1024 ** 3)
        capability = f"{props.major}.{props.minor}"
        print("-" * 60)
        print(f"GPU {index}: {torch.cuda.get_device_name(index)}")
        print(f"  计算能力: {capability}")
        print(f"  显存大小: {total_memory_gb:.2f} GB")
        print(f"  多处理器数量: {props.multi_processor_count}")

    try:
        device = torch.device("cuda:0")
        sample = torch.rand((1024, 1024), device=device)
        result = (sample @ sample).mean().item()
        torch.cuda.synchronize()
        print("-" * 60)
        print(f"[OK] GPU 张量计算测试通过，结果: {result:.6f}")
    except Exception as exc:
        print(f"[FAIL] GPU 张量计算测试失败: {exc}")


def print_summary(imported_modules: dict[str, Any]) -> None:
    print_header("4. 环境结论")
    missing_modules = [name for name in MODULES_TO_CHECK if name not in imported_modules]

    if missing_modules:
        print("以下模块缺失或导入失败：")
        for name in missing_modules:
            print(f"  - {name}")
    else:
        print("常用依赖模块检查通过。")

    torch = imported_modules.get("torch")
    if torch is None:
        print("未安装 PyTorch，当前无法使用 GPU，也无法运行 YOLO。")
    elif torch.cuda.is_available():
        print("GPU 可用，当前环境可以尝试使用 CUDA 训练或推理。")
    else:
        print("PyTorch 已安装，但 CUDA/GPU 当前不可用。")


def main() -> None:
    print("YOLO 环境检测工具")
    imported_modules = check_modules()
    check_python_environment()
    check_gpu(imported_modules)
    print_summary(imported_modules)


if __name__ == "__main__":
    main()
