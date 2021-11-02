import cv2
import mediapipe as mp

# Yüz algılama için gerekli kodların değişkenlere atanma işlemi
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

camera = cv2.VideoCapture(0)
while True:
    ret, cam_read = camera.read()
    h, w, _ = cam_read.shape
    cam_read = cv2.cvtColor(cam_read, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(cam_read)
    try:
        for face_landmarks in result.multi_face_landmarks:
            for i in range(0, 468):
                position1 = face_landmarks.landmark[i]
                x = int(position1.x * w)
                y = int(position1.y * h)
                cv2.circle(cam_read, (x, y), 1, (255, 0, 0))
                print("X ve Y", x, y)
    except:
        print("Yüz algilanamadi")
    rgb_to_bgr = cv2.cvtColor(cam_read, cv2.COLOR_RGB2BGR)
    cv2.imshow("Camera", rgb_to_bgr)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
cv2.destroyWindow()
