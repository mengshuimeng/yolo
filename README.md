1. 
```bash

scp -r <本地源路径> <用户名>@<远程IP>:<远程目标路径>
scp -r "D:\Documents\code\python\all_of_all\data_produce\datasets0321" jsh@192.168.0.214:/home/jsh/yolo/
```


2. 组织.yaml

3. yolo识别数据集
```
 conda activate yolo
 ```


···
yolo task=detect mode=train \
data=D:\Documents\code\python\yolo\yaml\4cjsjds.yaml \
model=yolo11s.pt \
epochs=200 \
batch=32 \
imgsz=768 \
lr0=0.001 \
optimizer=AdamW \
cos_lr=True \
device=0 \
patience=50 \
mosaic=0.5 \
mixup=0.1 \
workers=8 \
cache=True \
plots=True
```