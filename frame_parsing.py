import cv2
import time

# Путь к вашему видеофайлу
video_path = 'output_10_frames.mp4'  # замените на ваш файл

# Открытие видеопотока
cap = cv2.VideoCapture(video_path)

# Проверка успешного открытия видео
if not cap.isOpened():
    print("Ошибка открытия видеофайла")
    exit()

# Параметры кодека и выходного видеофайла
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None



start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width, channels = frame.shape

    # Ваша функция обработки кадра, если требуется
    # frame = frame_undistortion(ret, frame)  # Раскомментируйте и замените на свою функцию

    if person_detected_in_roi(frame):#здесь должна быть детекция человека!!!!!!!!!!!!!
        if out is None:
            start_time = time.time()
            fragment_filename = f'output_fragment_{int(start_time)}.mp4'
            out = cv2.VideoWriter(fragment_filename, fourcc, 20.0, (width, height))

        # Запись кадра в выходной файл, если человек обнаружен в зоне интереса
        out.write(frame)
        print(f'Записан кадр в файл {fragment_filename}')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()