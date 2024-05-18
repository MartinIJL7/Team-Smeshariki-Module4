import cv2
import numpy as np
def distortion(Video, dis_coeffs):
    # Загрузка видеопотока
    cap = cv2.VideoCapture(fr'{Video}')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('your_video.avi', fourcc, 20.0, size)
    # while True:
    #     ret, frame = cap.read()
    #     cv2.imshow('test', frame)
    # Параметры дисторсии
    dis_coeffs=dis_coeffs.split()
    dist_coeffs = np.array([float(dis_coeffs[0]), float(dis_coeffs[1]), float(dis_coeffs[2]), float(dis_coeffs[3]), float(dis_coeffs[4])])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Получение параметров камеры
        h, w = frame.shape[:2]
        focal_length = w

        camera_matrix = np.array([[float(dis_coeffs[5]), 0.00000000e+00, float(dis_coeffs[6])],
                                  [0.00000000e+00, float(dis_coeffs[7]), float(dis_coeffs[8])],
                                  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

        # Коррекция дисторсии
        undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coeffs)
        out.write(undistorted_frame)

        cv2.imshow('Undistorted Frame', undistorted_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()