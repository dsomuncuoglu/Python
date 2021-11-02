import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

capture = cv2.VideoCapture(0)
capture.set(3, 1280)
capture.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keyboardKeys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                ["Z", "X", "C", "V", "B", "N", "M", ".", ",", "/"]]
cikti = ""
klavye = Controller()


def createKeyboard(img, klavyeListesi):
    imgNew = np.zeros_like(img, np.uint8)
    for tus in klavyeListesi:
        x, y = tus.pos
        cvzone.cornerRect(imgNew, (tus.pos[0], tus.pos[1], tus.size[0], tus.size[1]), 20, rt=0)
        cv2.rectangle(imgNew, tus.pos, (x + tus.size[0], y + tus.size[1]), (255, 0, 0), cv2.FILLED)
        cv2.putText(imgNew, tus.text, (x + 12, y + 62), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255),
                    5)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    return out


class keyboard():
    def __init__(self, pos, text, size=[75, 75]):
        self.pos = pos
        self.text = text
        self.size = size


klavyeListesi = []
for x in range(len(keyboardKeys)):
    for i, key in enumerate(keyboardKeys[x]):
        klavyeListesi.append(keyboard([100 * i + 50, 100 * x + 50], key))

while True:
    success, img = capture.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = createKeyboard(img, klavyeListesi)

    if lmList:

        for tus in klavyeListesi:
            x, y = tus.pos
            w, h = tus.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, tus.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, tus.text, (x + 12, y + 62), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                # print(l)
                if l < 35:
                    klavye.press(tus.text)
                    cv2.rectangle(img, tus.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, tus.text, (x + 12, y + 62), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
                    cikti += tus.text
                    sleep(0.25)

    cv2.rectangle(img, (50, 350), (700, 450), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, cikti, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Camera", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
