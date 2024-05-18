import asyncio
import websockets
import json
import numpy as np
import math

# Внутренние параметры камеры
f_x, f_y = 1536 , 34865  # фокусные расстояния в пикселях (примерные значения)
c_x, c_y = 320, 240    # координаты центра изображения
K = np.array([[f_x, 0, c_x],
              [0, f_y, c_y],
              [0, 0, 1]])

# Функция для обработки данных телеметрии
def process_telemetry(data):
    latitude = data['latitude']
    longitude = data['longitude']
    rel_alt = data['rel_alt']
    drone_yaw = data['drone_yaw']
    drone_pitch = data['drone_pitch']
    drone_roll = data['drone_roll']

    yaw_rad = np.radians(drone_yaw)
    pitch_rad = np.radians(drone_pitch)
    roll_rad = np.radians(drone_roll)

    px, py = 320, 240

    uv1 = np.array([px, py, 1])
    K_inv = np.linalg.inv(K)
    xy_norm = K_inv @ uv1

    angle_x = np.arctan2(xy_norm[0], 1)
    angle_y = np.arctan2(xy_norm[1], 1)

    altitude = rel_alt
    gb_pitch = -70.0  
    gb_pitch_rad = np.radians(gb_pitch)
    depth = altitude / np.tan(gb_pitch_rad + angle_y)

    R_yaw = np.array([[math.cos(yaw_rad), -math.sin(yaw_rad), 0],
                      [math.sin(yaw_rad), math.cos(yaw_rad), 0],
                      [0, 0, 1]])

    R_pitch = np.array([[math.cos(pitch_rad), 0, math.sin(pitch_rad)],
                        [0, 1, 0],
                        [-math.sin(pitch_rad), 0, math.cos(pitch_rad)]])

    R_roll = np.array([[1, 0, 0],
                       [0, math.cos(roll_rad), -math.sin(roll_rad)],
                       [0, math.sin(roll_rad), math.cos(roll_rad)]])

    R = R_yaw @ R_pitch @ R_roll

    T = np.array([0, 0, altitude])

    dx = depth * np.tan(angle_x)
    dy = depth * np.tan(angle_y)
    dz = depth

    camera_coords = np.array([dx, dy, dz])

    world_coords = R.T @ camera_coords + T

    R_earth = 6378137  
    dlat = world_coords[1] / R_earth
    dlon = world_coords[0] / (R_earth * np.cos(np.radians(latitude)))

    new_latitude = latitude + np.degrees(dlat)
    new_longitude = longitude + np.degrees(dlon)

    print(f"Мировые координаты объекта: {new_latitude}, {new_longitude}")

async def telemetry_listener():
    uri = "ws://192.168.0.103:8555/ws"  
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            process_telemetry(data)

# Запуск асинхронного клиента
asyncio.get_event_loop().run_until_complete(telemetry_listener())