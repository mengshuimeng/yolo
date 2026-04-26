from ultralytics import YOLO

# 加载你的模型
model = YOLO("../jsjbest.pt")

# 打印所有类别（编号 + 名称）
print("模型所有类别：")
for k, v in model.names.items():
    print(f"编号 {k} : {v}")