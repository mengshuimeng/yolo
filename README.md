# YOLO 数据采集、标注与训练工具箱

这个仓库现在更适合按一条完整流水线来理解：

`录视频 -> 抽帧 -> 统一编号 -> 分发标注 -> XML转YOLO -> 切分训练集 -> 训练/推理`

当前 README 已按 `src/` 目录里的实际脚本更新，重点以这些文件为准：

- `src/01_capture_videos.py`
- `src/02_video_to_frames_numbered.py`
- `src/03_rename_picture.py`
- `src/04_distubute.py`
- `src/05_data_organize.py`
- `src/xml_to_yolo.py`
- `src/test_envirment.py`
- `src/find_classes.py`
- `src/test_model_grasp_cvison.py`

## 目录说明

- `src/`：核心脚本
- `videos/`：录制好的原始视频
- `datasets_original/`：原始图片、抽帧结果、重命名结果、分发结果
- `datasets_labeling/`：已经整理成训练集结构的数据
- `datasets/`：另一套训练集目录，部分脚本会默认写到这里
- `yaml/`：YOLO 数据集配置文件
- `pts/`：模型权重
- `runs/`：训练和推理输出

当前仓库里比较重要的现成目录包括：

- `datasets_original/20260426_dropzone1`：抽帧后的图片
- `datasets_original/20260426_dropzone2`：统一编号后的图片
- `datasets_original/20260426_dropzone2_distributed`：分发给多人标注的图片
- `datasets_labeling/datasets0321/defect`：已整理好的 YOLO 数据集示例
- `datasets_labeling/datasets/de`：另一套已整理好的 YOLO 数据集示例

## 环境准备

推荐直接使用你当前的 Conda 环境：

```powershell
conda activate yolo
pip install -r requirements.back.txt
```

先做环境自检：

```powershell
python .\src\test_envirment.py
```

这个脚本会检查：

- Python 版本和解释器路径
- `cv2`、`numpy`、`torch`、`torchvision`、`ultralytics`
- CUDA / cuDNN / GPU 信息
- GPU 张量计算是否能正常执行

## `src` 脚本说明

### `src/01_capture_videos.py`

用途：打开摄像头并录制视频。

特点：

- 自动保存到项目根目录下的 `videos/`
- 输出文件名格式为 `video_YYYYMMDD_HHMMSS.mp4`
- 默认目标帧率 `30`
- 会依次尝试摄像头索引 `0~10`
- 按 `q` 结束录制

运行方式：

```powershell
python .\src\01_capture_videos.py
```

### `src/02_video_to_frames_numbered.py`

用途：将视频拆成连续图片帧。

默认参数来自脚本当前内容：

- 输入视频：`videos\video_20260426_181953.mp4`
- 输出目录：`datasets_original\20260426_dropzone1`
- 图片格式：`jpg`
- 抽帧步长：`3`
- 起始编号：`1032`

输出文件名格式为 `0001.jpg`、`0002.jpg`。

运行方式：

```powershell
python .\src\02_video_to_frames_numbered.py
```

或手动指定：

```powershell
python .\src\02_video_to_frames_numbered.py `
  -i videos\video_20260426_181643.mp4 `
  -o datasets_original\20260426_dropzone1 `
  -f jpg `
  --step 3 `
  --start 1
```

说明：

- 相对路径会自动以项目根目录为基准
- 如果目标文件已存在，脚本会停止，避免覆盖旧数据

### `src/03_rename_picture.py`

用途：将图片重新整理成连续编号。

默认参数：

- 输入目录：`datasets_original\20260426_dropzone1`
- 输出目录：`datasets_original\20260426_dropzone2`
- 起始编号：`1`

输出文件名固定为四位前导零格式，例如：

- `0001.jpg`
- `0002.jpg`
- `0100.jpg`

运行方式：

```powershell
python .\src\03_rename_picture.py
```

或手动指定：

```powershell
python .\src\03_rename_picture.py `
  -i datasets_original\20260426_dropzone1 `
  -o datasets_original\20260426_dropzone2 `
  -s 1
```

说明：

- 使用自然排序，避免 `1.jpg、10.jpg、2.jpg` 这种错序
- 输出统一保存为 `.jpg`
- 如果目标文件已存在，脚本会停止

### `src/04_distubute.py`

用途：把一批图片均分给多人标注。

默认参数：

- 源目录：`datasets_original\20260426_dropzone2`
- 人数：`11`
- 输出目录：`datasets_original\20260426_dropzone2_distributed`

运行方式：

```powershell
python .\src\04_distubute.py
```

或手动指定：

```powershell
python .\src\04_distubute.py `
  --source_folder datasets_original\20260426_dropzone2 `
  --num_people 11 `
  --output_folder datasets_original\20260426_dropzone2_distributed
```

说明：

- 每个人的子文件夹名称是该组的起始编号
- 图片按自然排序后再均分
- 如果输出位置已有同名文件，脚本会停止

### `src/xml_to_yolo.py`

用途：把 Pascal VOC XML 标注转换成 YOLO `.txt` 标注。

这个脚本当前不是命令行参数版，而是脚本内常量版。运行前要先修改：

- `CLASS_MAPPING`
- `XML_DIR`
- `OUTPUT_TXT_DIR`

当前示例写法是：

```python
XML_DIR = "D:\\Desktop\\temp\\labels"
OUTPUT_TXT_DIR = "D:\\Desktop\\temp\\1"
CLASS_MAPPING = {
    "0": 0
}
```

运行方式：

```powershell
python .\src\xml_to_yolo.py
```

说明：

- 每个 XML 会输出一个同名 `.txt`
- 即使某张图片没有目标，也会创建空标签文件
- 运行前务必把类别映射改成你自己的类别

### `src/05_data_organize.py`

用途：把图片和标签切分成 `train / val / test`。

这个脚本当前也是“修改顶部参数后直接运行”的风格。重点变量：

- `DATASET_NAME`
- `train_percent`
- `val_percent`
- `test_percent`
- `root`

当前脚本里的默认值是：

```python
DATASET_NAME = "4cjsjds"
train_percent = 0.8
val_percent = 0.1
test_percent = 0.1
root = "D:\\Documents\\code\\python\\yolo\\datasets\\4cjsjds"
```

脚本会生成：

```text
datasets/<DATASET_NAME>/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
├── train.txt
├── val.txt
└── test.txt
```

运行方式：

```powershell
python .\src\05_data_organize.py
```

说明：

- 当前脚本会写入项目根目录下的 `datasets/`
- 不是写入 `datasets_labeling/`
- 每次运行会清空目标训练/验证/测试目录中的原有文件

### `src/find_classes.py`

用途：查看模型类别名。

当前脚本默认读取：

```python
YOLO("../jsjbest.pt")
```

运行方式：

```powershell
python .\src\find_classes.py
```

如果你的权重实际在 `pts/` 下，建议先把脚本中的模型路径改掉。

### `src/test_model_grasp_cvison.py`

用途：对单张图片或整个文件夹做推理。

当前默认模型路径写死为：

```python
D:\Documents\code\python\yolo\grasp_detector.pt
```

运行方式：

```powershell
python .\src\test_model_grasp_cvison.py D:\path\to\image_or_folder
```

说明：

- 支持单张图片
- 支持整个文件夹批量推理
- 默认会保存结果到 `runs/detect/predict/`

## 一套可复刻的流程

下面这套流程最适合你现在这个仓库。

### 1. 检查环境

```powershell
python .\src\test_envirment.py
```

确认以下几点都通过：

- `torch` 可导入
- `CUDA 是否可用: True`
- GPU 张量计算测试通过

### 2. 录制原始视频

```powershell
python .\src\01_capture_videos.py
```

录完后视频会保存在：

```text
videos/
```

### 3. 从视频抽帧

```powershell
python .\src\02_video_to_frames_numbered.py `
  -i videos\video_20260426_181953.mp4 `
  -o datasets_original\20260426_dropzone1 `
  -f jpg `
  --step 3 `
  --start 1
```

输出目录：

```text
datasets_original\20260426_dropzone1
```

### 4. 统一图片编号

```powershell
python .\src\03_rename_picture.py `
  -i datasets_original\20260426_dropzone1 `
  -o datasets_original\20260426_dropzone2 `
  -s 1
```

输出结果会统一成：

```text
0001.jpg
0002.jpg
0003.jpg
...
```

### 5. 分发给多人标注

```powershell
python .\src\04_distubute.py `
  --source_folder datasets_original\20260426_dropzone2 `
  --num_people 11 `
  --output_folder datasets_original\20260426_dropzone2_distributed
```

这一步完成后，把分发出去的图片分别标注成 XML。


### 6. 准备 `images/` 和 `labels/`

在一个数据集根目录下整理成这种结构：

```text
你的数据集目录/
├── images/
│   ├── 0001.jpg
│   ├── 0002.jpg
│   └── ...
└── labels/
    ├── 0001.txt
    ├── 0002.txt
    └── ...
```

这个目录可以放在：

- `datasets/你的数据集名`
- 或 `datasets_labeling/你的数据集名`

但如果你要直接跑 `src/05_data_organize.py`，就要把它的 `root` 改成实际路径。

### 7. 切分训练集

先修改 `src/05_data_organize.py` 顶部配置，再运行：

```powershell
python .\src\05_data_organize.py
```

切分完成后，脚本会在 `datasets/<DATASET_NAME>/` 下生成：

- `images/train`
- `images/val`
- `images/test`
- `labels/train`
- `labels/val`
- `labels/test`
- `train.txt`
- `val.txt`
- `test.txt`

### 8. 修改 YAML 并开始训练

当前仓库里的 YAML 包括：

- `yaml/4cjsjds.yaml`
- `yaml/box_datasets0321.yaml`
- `yaml/datasets.yaml`
- `yaml/ict_datasets.yaml`
- `yaml/ict_datasets_ugkz.yaml`

使用前先检查里面的 `train / val / test` 路径是否对应你实际生成的数据集。

训练命令示例：

```powershell
yolo task=detect mode=train `
  data=yaml\4cjsjds.yaml `
  model=pts\yolo11s.pt `
  epochs=200 `
  batch=32 `
  imgsz=768 `
  lr0=0.001 `
  optimizer=AdamW `
  cos_lr=True `
  device=0 `
  patience=50 `
  mosaic=0.5 `
  mixup=0.1 `
  workers=8 `
  cache=True `
  plots=True
```

### 9. 训练后检查类别和推理效果

查看类别：

```powershell
python .\src\find_classes.py
```

执行推理：

```powershell
python .\src\test_model_grasp_cvison.py D:\path\to\image_or_folder
```

## YAML 文件说明

- `yaml/4cjsjds.yaml`：1 类，`fire_extinguisher`
- `yaml/box_datasets0321.yaml`：4 类，`0 / 1 / 2 / 3`
- `yaml/datasets.yaml`：4 类，`0 / 1 / 2 / 3`
- `yaml/ict_datasets.yaml`：1 类，`ug`
- `yaml/ict_datasets_ugkz.yaml`：2 类，`ug / kz`

## 当前脚本的注意事项

这部分很重要，别等跑炸了再回来看。

- `src/xml_to_yolo.py` 依赖脚本内手工改路径和类别映射，不是命令行参数版
- `src/05_data_organize.py` 当前包含绝对路径配置，换机器或换目录后必须改
- `src/05_data_organize.py` 默认输出到 `datasets/`，不是 `datasets_labeling/`
- `src/find_classes.py` 当前模型路径写的是 `../jsjbest.pt`，和 `pts/` 目录不完全一致
- `src/test_model_grasp_cvison.py` 默认模型路径是绝对路径，换环境后建议改成相对路径
- `yaml/4cjsjds.yaml` 当前路径写到了 `src/datasets/4cjsjds/...`，使用前必须核对
- `yaml/ict_datasets_ugkz.yaml` 当前 `train / val / test` 都指向 `train.txt`，训练前建议修正

## 建议的后续整理方向

如果你接下来要继续把这个仓库长期用下去，最值得做的是这三件事：

1. 把 `xml_to_yolo.py` 改成命令行参数版
2. 把 `05_data_organize.py` 改成相对路径版
3. 把 `find_classes.py` 和 `test_model_grasp_cvison.py` 的模型路径统一到 `pts/`

这样 README、目录、脚本就能真正闭环，不会再出现“文档一套、代码一套、路径又一套”的情况。
