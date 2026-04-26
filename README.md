# YOLO 数据处理与训练工具箱

这个仓库是一个面向 YOLO 的数据制作、训练和推理工作区，当前目录更适合按下面这条线理解：

`原始素材 -> 处理区 -> 最终数据集 -> 训练/推理`

## 目录约定

- `datasets_original/`：原始数据归档
- `datasets_produce/`：处理中间产物和最终训练集
- `src/`：所有处理脚本
- `yaml/`：YOLO 数据集配置
- `videos/`：原始视频
- `runs/`：训练和推理输出
- `pts/`：模型权重

### `datasets_original/`

- `0321/`：原始图片素材
- `extinguisher/`：另一套原始素材
- `output/`：原始输出结果

### `datasets_produce/`

- `1212/`：统一编号后的图片
- `jsj/`：视频抽帧结果
- `datasets0321/defect/`：已经组织好的训练数据集
- `datasets/defect/`：另一份同结构数据集
- `data/`、`output/`：中间产物

## 环境准备

```bash
conda activate yolo
pip install -r requirements.back.txt
```

## 脚本说明

- `src/capture_videos.py`：录制摄像头视频
- `src/video_to_frames_numbered.py`：视频抽帧
- `src/rename_picture.py`：图片批量重命名
- `src/distubute.py`：图片按人数/文件夹均分
- `src/xml_to_yolo.py`：XML 转 YOLO txt
- `src/data_organize.py`：切分 train/val/test
- `src/test_model_grasp_cvison.py`：模型推理
- `src/find_classes.py`：查看模型类别

## 可复刻流程

### 1. 准备原始素材

把原始视频放到 `videos/`，或把原始图片放到 `datasets_original/0321/`。

### 2. 视频抽帧

```bash
python src/video_to_frames_numbered.py -i videos/xxx.mp4 -o datasets_produce/jsj --step 1 --start 1
```

如果你已经有图片，只想统一编号：

```bash
python src/rename_picture.py -i datasets_original/0321 -o datasets_produce/1212 -s 1
```

### 3. 标注转 YOLO

先用标注工具导出 XML，再修改 `src/xml_to_yolo.py` 里的：

- `XML_DIR`
- `OUTPUT_TXT_DIR`
- `CLASS_MAPPING`

然后运行：

```bash
python src/xml_to_yolo.py
```

### 4. 切分数据集

先修改 `src/data_organize.py` 里的：

- `DATASET_NAME`
- `root`
- `train_percent`
- `val_percent`
- `test_percent`

然后运行：

```bash
python src/data_organize.py
```

输出结构会类似：

- `datasets_produce/datasets0321/defect/images/train`
- `datasets_produce/datasets0321/defect/images/val`
- `datasets_produce/datasets0321/defect/images/test`
- `datasets_produce/datasets0321/defect/labels/train`
- `datasets_produce/datasets0321/defect/labels/val`
- `datasets_produce/datasets0321/defect/labels/test`
- `datasets_produce/datasets0321/defect/train.txt`
- `datasets_produce/datasets0321/defect/val.txt`
- `datasets_produce/datasets0321/defect/test.txt`

### 5. 配置训练

当前训练配置示例在 [`yaml/4cjsjds.yaml`](yaml/4cjsjds.yaml)。

如果你使用 `datasets_produce/datasets0321/defect/`，建议把 yaml 改成对应路径；`datasets_produce/datasets0321/datasets.yaml` 也可以作为模板，但里面的路径要改成你本机实际仓库位置。

训练命令示例：

```bash
yolo task=detect mode=train ^
data=yaml/4cjsjds.yaml ^
model=yolo11s.pt ^
epochs=200 ^
batch=32 ^
imgsz=768 ^
lr0=0.001 ^
optimizer=AdamW ^
cos_lr=True ^
device=0 ^
patience=50 ^
mosaic=0.5 ^
mixup=0.1 ^
workers=8 ^
cache=True ^
plots=True
```

### 6. 推理验证

```bash
python src/test_model_grasp_cvison.py D:\path\to\image_or_folder
```

## YAML 说明

- `yaml/4cjsjds.yaml`：1 类，`fire_extinguisher`
- `yaml/datasets.yaml`：4 类，`0/1/2/3`
- `yaml/ict_datasets.yaml`：1 类，`ug`
- `yaml/ict_datasets_ugkz.yaml`：2 类，`ug/kz`
- `yaml/box_datasets0321.yaml`：4 类，`0/1/2/3`

## 注意事项

- `data_organize.py` 里的默认路径和当前目录不一定一致，运行前先改。
- `xml_to_yolo.py` 里的类别映射要先换成你自己的类别。
- `datasets_original/` 适合放原始归档，`datasets_produce/` 适合放处理结果。
- `runs/`、`pts/`、`output/` 这类产物建议只保留结果，不要混进原始素材。

## 远程传输

```bash
scp -r "D:\Documents\code\python\all_of_all\data_produce\datasets0321" jsh@192.168.0.214:/home/jsh/yolo/
```
