import cv2
from cvzone.HandTrackingModule import HandDetector


camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

detector = HandDetector(detectionCon=0.8)
b_Degeri = None
olcum = 0
cx, cy = 200, 200

while True:
    ret, cam_read = camera.read()
    hands, cam_read = detector.findHands(cam_read)
    img_read = cv2.imread("resim.jpeg")
    if len(hands) == 2:
        if detector.fingersUp(hands[0]) == [0, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [0, 1, 0, 0, 0]:
            print("Yakinlastirma ve uzaklastirma islemleri gerceklesiyor.")
            lmList_L = hands[0]["lmList"]
            lmList_R = hands[1]["lmList"]
            # Iki el arasindaki mesafe olcme
            if b_Degeri is None:
                length, info, cam_read = detector.findDistance(lmList_L[8], lmList_R[8], cam_read)
                # print("Uzunluk: ", uzunluk)
                b_Degeri = length
            length, info, cam_read = detector.findDistance(lmList_L[8], lmList_R[8], cam_read)
            olcum = (int(length - b_Degeri) // 2)
            cx, cy = info[4:]
            if olcum > 0:
                print("Yakinlasma : ", olcum)
            else:
                print("Uzaklasma", olcum)
    else:
        b_Degeri = None
    try:
        h1, w1, _ = img_read.shape
        newH, newW = ((h1 + olcum) // 2) * 2, ((w1 + olcum) // 2) * 2
        img_read = cv2.resize(img_read, (newW, newH))

        cam_read[cy - newH // 2:cy + newH // 2, cx - newW // 2:cx + newW // 2] = img_read
    except:
        pass
    cv2.imshow("Kamera", cam_read)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
