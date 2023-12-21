from ultralytics import YOLO

def object_detection(images, model_path):
    model = YOLO(model_path)
    results = model(images)
    detection_data = []
    for result in results:
        boxes = result.boxes.xyxy
        classes = [model.names[int(cls)] for cls in result.boxes.cls if cls.nelement() > 0]
        detection_data.append({"boxes": boxes.tolist(), "classes": classes})
    return detection_data
