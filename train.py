from ultralytics import YOLO

model = YOLO("../pretrained/yolov8n.pt")

results = model.train(data="dataset.yaml", epochs=50, cache="ram", pretrained=True)
results = model.val()
success = model.export(format="onnx")  # export the model to ONNX format

