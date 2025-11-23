"""
该脚本用于检测和验证深度学习开发环境的配置情况，主要检查Python、PyTorch和Ultralytics YOLO框架的版本信息以及GPU支持状态。

功能说明：
- 检测当前Python解释器版本
- 显示PyTorch库版本和CUDA版本信息
- 验证CUDA是否可用，判断是否支持GPU加速
- 如果GPU可用，显示当前GPU设备名称
- 展示Ultralytics库的版本号
- 运行Ultralytics的系统兼容性检查

输入参数：无（自动从系统环境中获取信息）

输出信息：
1. Python版本号（从 `sys.version` 获取）
2. PyTorch版本（通过 `torch.__version__` 获取）
3. CUDA版本（通过 `torch.version.cuda` 获取）
4. CUDA可用性状态（通过 `torch.cuda.is_available()` 检查）
5. GPU设备名称（当CUDA可用时，通过 `torch.cuda.get_device_name(0)` 获取）
6. Ultralytics版本（通过 `ultralytics.__version__` 获取）
7. Ultralytics系统检查详细报告（通过 `ultralytics.checks()` 执行）

此脚本通常用于开发环境初始化时验证配置是否正确，特别是确认GPU支持是否正常工作。
"""

import torch, ultralytics, sys

print("python", sys.version.split()[0])
print("torch:", torch.__version__, "cuda:", torch.version.cuda)
print("cuda available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("device:", torch.cuda.get_device_name(0))
print("ultralytics:", ultralytics.__version__)
ultralytics.checks()
