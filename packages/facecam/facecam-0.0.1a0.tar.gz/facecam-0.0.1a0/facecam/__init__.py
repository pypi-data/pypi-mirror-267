import cv2
import numpy as np
import os
import time
import imageio

d = os.path.dirname(__file__)

def get_path(relative):
    return os.path.join(d, relative)

# Define paths for images
RABBIT = get_path("resources/img/rabbit.png")
TIE = get_path("resources/img/tie.png")
BAND = get_path("resources/img/band.png")
BEARD = get_path("resources/img/beard.png")
CAT = get_path("resources/img/cat.png")
FLOWER = get_path("resources/img/flower.png")
GLASS1 =get_path("resources/img/glass_1.png")
GLASS2 = get_path("resources/img/glass_2.png")
HAT = get_path("resources/img/hat.png")
HEART = get_path("resources/img/heart.png")
NOSE = get_path("resources/img/nose.png")
MOUTH1 =get_path("resources/img/mouth_1.png")
MOUTH2 = get_path("resources/img/mouth_2.png")
TIGER = get_path("resources/img/tiger.png")
MASK1 = get_path("resources/img/mask_1.png")
MASK2 = get_path("resources/img/mask_2.png")

# Initialize video capture
cap = cv2.VideoCapture(0)

_, frame = cap.read()
frame = cv2.flip(frame, 1)
k = ""
v_s = 0
v_t = 0
t = time.time()

# Load Haar cascade for face detection
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ===============

# 模型和配置文件的路径
modelFile = get_path("resources/opencv_face_detector_uint8.pb")
configFile = get_path("resources/opencv_face_detector.pbtxt")

# 加载模型
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

# ============

def get_face():
    # 获取帧的维度并转换为blob
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # 设置blob作为网络的输入
    net.setInput(blob)
    detections = net.forward()

    # 循环遍历检测到的人脸
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]  # 检测的置信度
        if confidence > 0.5:  # 置信度阈值
            # 计算人脸的边界框
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype("int")
            return startX, startY, endX, endY

    return 0, 0, 0, 0

def add_text_to_image_opencv(image, text, font_scale=0.7, color=(255, 255, 255), position=(10, 50), thickness=2):
    """
    Add text to an image using OpenCV.
    :param image: OpenCV image array.
    :param text: String of text to add to the image.
    :param font_scale: Scale of the font.
    :param color: Color of the font in BGR.
    :param position: Bottom-left corner of the text string in the image.
    :param thickness: Thickness of the lines used to draw the text.
    """
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, position, font_face, font_scale, color, thickness, lineType=cv2.LINE_AA)

def paste(dir, r_y, r_x):
    # 首先，获取人脸的位置
    x1, y1, x2, y2 = get_face()
    if x2 > 0:  # 确保检测到了人脸
        # 加载源图像
        src_image = cv2.imread(dir, cv2.IMREAD_UNCHANGED)
        if src_image is None:
            return  # 图像加载失败

        # 计算目标位置和大小
        mid_x = (x2 + x1) // 2
        face_width = x2 - x1
        width = int(face_width * r_x / 100)
        height = int(src_image.shape[0] * (width / src_image.shape[1]))
        x1 = int(mid_x - width / 2)
        x2 = int(mid_x + width / 2)
        y = int(y1 + (y2 - y1) * r_y / 100 - height)

        # 调整源图像大小以适应目标区域
        src_image_resized = cv2.resize(src_image, (width, height), interpolation=cv2.INTER_AREA)

        # 如果源图像有透明通道，则处理透明度
        if src_image_resized.shape[2] == 4:
            overlay_image(frame, src_image_resized, (x1, y))
        else:
            frame[y:y + height, x1:x1 + width] = src_image_resized


def overlay_image(dest_img, src_img, position):
    x, y = position
    # 计算覆盖区域的维度
    width, height = src_img.shape[1], src_img.shape[0]

    # 确保覆盖区域完全在目标图像内部
    x_end = min(x + width, dest_img.shape[1])
    y_end = min(y + height, dest_img.shape[0])
    width = x_end - x
    height = y_end - y

    # 如果位置超出目标图像边界，则不执行覆盖操作
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        return

    # 调整源图像大小以适应目标区域（如果需要）
    src_img_resized = cv2.resize(src_img, (width, height), interpolation=cv2.INTER_AREA)

    # 提取alpha通道用作掩码
    alpha_s = src_img_resized[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    # 对于每个通道进行合成
    for c in range(0, 3):
        dest_img[y:y_end, x:x_end, c] = (alpha_s * src_img_resized[:, :, c] +
                                         alpha_l * dest_img[y:y_end, x:x_end, c])

def gif(key, dir, timelimit=5, max_width=475, max_height=350, text=""):
    dir += ".gif"
    global v_t, v_s, frame
    if k == key:  # 这里应该有一个条件来判断是否开始或停止录制
        if not v_t:
            v_s = t
            v_t = t
            if not os.path.exists(".temp"):
                os.mkdir(".temp")
            else:
                for f in os.listdir(".temp"):
                    os.remove(".temp/{}".format(f))
        else:
            frames = optimize_frames_opencv(".temp", max_width, max_height, text)
            imageio.mimsave(dir, frames, 'GIF', duration=0.2)
            cleanup_temp()
    if v_s and t - v_s > timelimit:
        frames = optimize_frames_opencv(".temp", max_width, max_height, text)
        imageio.mimsave(dir, frames, 'GIF', duration=0.2)
        cleanup_temp()
    if v_t and t - v_t >= 0.2:
        cv2.imwrite(".temp/{:.0f}.png".format(time.time() * 100), cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA))
        v_t = t

def cleanup_temp():
    for f in os.listdir(".temp"):
        os.remove(".temp/{}".format(f))
    global v_s, v_t
    v_s = 0
    v_t = 0

def catch():
    global frame, t
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    t = time.time()

def get_key():
    return k

def display():
    global k
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k >= 0:
        k = chr(k)
    else:
        k = ""

def quit():
    cv2.destroyAllWindows()
    cap.release()

def face(rect=1):
    if rect:
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
        )
        net.setInput(blob)
        detections = net.forward()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < 0.75:
                continue
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
        return

def optimize_frames_opencv(temp_dir, max_width, max_height, text=""):
    frames = []
    for f in sorted(os.listdir(temp_dir), key=lambda x: int(x.split('.')[0])):
        img_path = os.path.join(temp_dir, f)
        img = cv2.imread(img_path)

        h, w = img.shape[:2]
        if w > max_width or h > max_height:
            scale_w = max_width / w
            scale_h = max_height / h

            scale = min(scale_w, scale_h)
            new_width = int(w * scale)
            new_height = int(h * scale)

            img = cv2.resize(img, (new_width, new_height))

        # 如果需要，在图像上添加文本
        if text:
            add_text_to_image_opencv(img, text, position=(10, 50), font_scale=1, color=(255, 255, 255), thickness=2)

        # OpenCV 默认使用 BGR，imageio 需要 RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frames.append(img)
    return frames




