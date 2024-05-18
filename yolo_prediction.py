import torch
import cv2
from pathlib import Path
from time import time

# Загрузка модели
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

# Путь к входному видео
video_path = 'input_video.mp4'
cap = cv2.VideoCapture(video_path)

# Путь к выходному видео
output_path = 'output_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Обработка кадра
    results = model(frame)

    # Отображение результатов на кадре
    for *box, conf, cls in results.xyxy[0]:
        label = f'{model.names[int(cls)]} {conf:.2f}'
        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
        cv2.putText(frame, label, (int(box[0]), int(box[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Запись кадра в выходной файл
    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()
