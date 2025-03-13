import os
import base64
import cv2
import pyautogui
import numpy as np
import mediapipe as mp
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

# Khởi tạo Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def base64_to_image(base64_string):
    """
    The base64_to_image function accepts a base64 encoded string and returns an image.
    The function extracts the base64 binary data from the input string, decodes it, converts 
    the bytes to numpy array, and then decodes the numpy array as an image using OpenCV.
    
    :param base64_string: Pass the base64 encoded image string to the function
    :return: An image
    """
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

def estimate_head_pose(image):
    """ Xác định hướng đầu từ ảnh """
    img_h, img_w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    face_3d = []
    face_2d = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [33, 263, 1, 61, 291, 199]:
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_2d.append([x, y])
                    face_3d.append([x, y, lm.z])

                    if idx == 1:  # Mũi
                        nose_2d = (x, y)
                        nose_3d = (x, y, lm.z * 3000)

        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        # Thiết lập ma trận camera
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_h / 2],
                               [0, focal_length, img_w / 2],
                               [0, 0, 1]])
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        # Giải phương trình PnP
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
        rmat, _ = cv2.Rodrigues(rot_vec)
        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

        x = angles[0] * 360
        y = angles[1] * 360

        # Xác định hướng đầu
        if y < -10:
            head_pose = "Looking Right" # Ảnh bị ngược nên đảo hướng
            action = "move_right"
        elif y > 10:
            head_pose = "Looking Left" # Ảnh bị ngược nên đảo hướng
            action = "move_left"
        elif x < -6:
            head_pose = "Looking Down"
            action = "move_down"
        elif x > 16:
            head_pose = "Looking Up"
            action = "move_up"
        else:
            head_pose = "Forward"
            action = "stay"

        return head_pose, action
    return "No Face Detected", "stay"

def move_mouse(action):
    """ Điều khiển chuột trên client """
    step = 30  # Khoảng cách di chuyển chuột mỗi lần
    x, y = pyautogui.position()

    if action == "move_left":
        pyautogui.moveTo(x - step, y)
    elif action == "move_right":
        pyautogui.moveTo(x + step, y)
    elif action == "move_up":
        pyautogui.moveTo(x, y - step)
    elif action == "move_down":
        pyautogui.moveTo(x, y + step)

def scroll_screen(action):
    """ Cuộn màn hình trên client """
    scroll_amount = 60

    if action == "move_up":
        pyautogui.scroll(scroll_amount)  
    elif action == "move_down":
        pyautogui.scroll(-scroll_amount)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # socketio.emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(data):
    """
    The receive_image function takes in an image from the webcam, converts it to grayscale, and then emits
    the processed image back to the client.


    :param image: Pass the image data to the receive_image function
    :return: The image that was received from the client
    """
    # Decode the base64-encoded image data
    image = base64_to_image(data["image"])
    mode = data["mode"]
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # frame_resized = cv2.resize(gray, (640, 360))
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    # result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    # processed_img_data = base64.b64encode(frame_encoded).decode()
    # b64_src = "data:image/jpg;base64,"
    # processed_img_data = b64_src + processed_img_data
    # socketio.emit("processed_image", processed_img_data)
    head_direction, mouse_action = estimate_head_pose(image)
    if mode == "cursor":
        move_mouse(mouse_action)
    else:
        scroll_screen(mouse_action)
    socketio.emit("head_pose", {"direction": head_direction, "mouse_action": mouse_action, "mode": mode})


@app.route('/')
def index():
    return jsonify({"message": "Server is running"})

if __name__ == '__main__':
    socketio.run(app, debug=True)