import cv2
import mediapipe as mp

# Yüz algılama için gerekli kodların değişkenlere atanma işlemi
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Resmin diskten okunması
img = cv2.imread("resim.jpeg")

h, w, _ = img.shape


# Orjinal resmin gösterilmesi
cv2.imshow("Orjinal Resim", img)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = face_mesh.process(img)



for face_landmarks in result.multi_face_landmarks:
    for i in range(0, 468):
        position1 = face_landmarks.landmark[i]
        x = int(position1.x * w)
        y = int(position1.y * h)
        cv2.circle(img, (x, y), 1, (0, 0, 255))
        print("X ve Y", x, y)

cv2.imshow("Face Mesh", img)

cv2.waitKey(0)
cv2.destroyWindow()
