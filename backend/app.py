import math
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

def rotation_matrix_to_angles(rotation_matrix):
    """
    Calculate Euler angles from rotation matrix.
    :param rotation_matrix: A 3*3 matrix with the following structure
    [Cosz*Cosy  Cosz*Siny*Sinx - Sinz*Cosx  Cosz*Siny*Cosx + Sinz*Sinx]
    [Sinz*Cosy  Sinz*Siny*Sinx + Sinz*Cosx  Sinz*Siny*Cosx - Cosz*Sinx]
    [  -Siny             CosySinx                   Cosy*Cosx         ]
    :return: Angles in degrees for each axis
    """
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 +
                                                     rotation_matrix[1, 0] ** 2))
    z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    return np.array([x, y, z]) * 180. / math.pi

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

    face_coordination_in_real_world = np.array([
        [285, 528, 200],
        [285, 371, 152],
        [197, 574, 128],
        [173, 425, 108],
        [360, 574, 128],
        [391, 425, 108]
    ], dtype=np.float64)
    face_coordination_in_image = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [1, 9, 57, 130, 287, 359]:
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    face_coordination_in_image.append([x, y])

        face_coordination_in_image = np.array(face_coordination_in_image,
                                                dtype=np.float64)

        # The camera matrix
        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, img_w / 2],
                                [0, focal_length, img_h / 2],
                                [0, 0, 1]])

        # The Distance Matrix
        dist_matrix = np.zeros((4, 1), dtype=np.float64)

        # Use solvePnP function to get rotation vector
        success, rotation_vec, transition_vec = cv2.solvePnP(
            face_coordination_in_real_world, face_coordination_in_image,
            cam_matrix, dist_matrix)

        # Use Rodrigues function to convert rotation vector to matrix
        rotation_matrix, jacobian = cv2.Rodrigues(rotation_vec)

        result = rotation_matrix_to_angles(rotation_matrix)

        pitch, yaw, roll = map(int, result)

        # Xác định hướng đầu
        if yaw <= -30:
            head_pose = "Looking Right" # Ảnh bị ngược nên đảo hướng
            action = "move_right"
        elif yaw >= 30:
            head_pose = "Looking Left" # Ảnh bị ngược nên đảo hướng
            action = "move_left"
        elif pitch <= -5 and 20 >= yaw >= -20 and 5 >= roll >= -5:
            head_pose = "Looking Down"
            action = "move_down"
        elif pitch >= 25 and 20 >= yaw >= -20 and 5 >= roll >= -5:
            head_pose = "Looking Up"
            action = "move_up"
        elif 20 > pitch >= 0 and 20 >= yaw >= -20 and roll <= -20:
            head_pose = "Tilt Right"
            action = "click_right"
        elif 20 > pitch >= 0 and 20 >= yaw >= -20 and roll >= 20:
            head_pose = "Tilt Left"
            action = "click_left"
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
    elif action == "click_left":
        pyautogui.click()
    elif action == "click_right":
        pyautogui.rightClick()

def scroll_screen(action):
    """ Cuộn màn hình trên client """
    scroll_amount = 250

    if action == "move_left":
        pyautogui.scroll(scroll_amount)  
    elif action == "move_right":
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