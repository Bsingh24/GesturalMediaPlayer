import cv2
import numpy as np
import mediapipe
import time
import HandTrackingModule as htm
import math
import pyautogui

import os
from playsound import playsound


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################

wcam = 1280
hcam = 720
midcam = hcam/2

################

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
val = 0
volBar = 400



globTF = 0
playpauseTF = 0
tempy1 = 0
tempy2 = 0
tempy3 = 0
tempy4 = 0
tempy5 = 0
tempx1 = 0
tempx2 = 0
tempx3 = 0
tempx4 = 0
tempx5 = 0

t = time.perf_counter()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        palmx,palmy = lmList[0][1],lmList[0][1]
        thumbx, thumby = lmList[4][1], lmList[4][2] #Thumb
        index_x, index_y = lmList[8][1], lmList[8][2] #Index Finger
        middle_x, middle_y = lmList[12][1], lmList[12][2] #Middle Finger
        ring_x, ring_y = lmList[16][1], lmList[16][2] #Ring Finger
        pinky_x, pinky_y = lmList[20][1], lmList[20][2] #Pinky Finger

        cv2.circle(img, (thumbx, thumby), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (middle_x, middle_y), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (ring_x, ring_y), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (pinky_x, pinky_y), 15, (255, 0, 255), cv2.FILLED)

        xc,yc = (thumbx + index_x) // 2, (thumby + index_y) // 2


        # if (index_y < thumby) and (middle_y < thumby) and (ring_y < thumby) and (pinky_y < thumby):
        #     tempy1 = 0
        #     tempy2 = 0
        #     tempy3 = 0
        #     tempy4 = 0
        #     tempy5 = 0
        #     tempx1 = 0
        #     tempx2 = 0
        #     tempx3 = 0
        #     tempx4 = 0
        #     tempx5 = 0
        #     globTF = 0
        #     playpauseTF = 0
        #
        # # these are the lower the level
        # if (index_y > thumby) and (middle_y < thumby) and (ring_y < thumby) and (pinky_y < thumby):  # index finder
        #     pyautogui.hotkey('volumedown')
        # elif (middle_y > thumby) and (index_y < thumby) and (ring_y < thumby) and (pinky_y < thumby):  # middle finger
        #     pyautogui.hotkey('volumeup')
        # elif (ring_y > thumby) and (index_y < thumby) and (middle_y < thumby) and (pinky_y < thumby):  # ring finger
        #     pyautogui.hotkey('stop')
        # elif (pinky_y > thumby) and (index_y < thumby) and (middle_y < thumby) and (ring_y < thumby):  # pinky finger
        #     if (playpauseTF == 0):
        #         pyautogui.hotkey('playpause')
        #         playpauseTF = 1
        #
        # # something a little more advanced
        # # hold hand like a gun with index_y and middle_y in the air, with ring_y and pinky_y pointed down. Then move thumby upwards to hand. to cancel just move hand or release hand.
        # if (index_y < thumby) and (middle_y < thumby) and (ring_y > thumby) and (pinky_y > thumby):
        #     # keeps track where the values are at before hand
        #     if (globTF == 0):
        #         tempy1 = thumby
        #         tempy2 = index_y
        #         tempy3 = middle_y
        #         tempy4 = ring_y
        #         tempy5 = pinky_y
        #         tempx1 = thumbx
        #         tempx2 = index_x
        #         tempx3 = middle_x
        #         tempx4 = ring_x
        #         tempx5 = pinky_x
        #         globTF = 1
        #     if (index_y < thumby) and (middle_y < thumby) and (ring_y > thumby) and (pinky_y > thumby) and (pinky_x < tempx1) and (thumbx > tempx5):
        #         if (index_y < (tempy2) - 15):
        #             print("gun too high!")
        #         elif (middle_y < (tempy3) - 15):
        #             print("gun too high!")
        #         elif (thumby < (tempy1) - 20):
        #             audio_file = os.path.dirname(__file__) + '/sounds/gunshot.mp3'
        #             #playsound(audio_file)
        #             print('I am Here')
        #             globTF = 0
        #             tempy1 = 0
        #             tempy2 = 0
        #             tempy3 = 0
        #             tempy4 = 0
        #             tempy5 = 0
        #             tempx1 = 0
        #             tempx2 = 0
        #             tempx3 = 0
        #             tempx4 = 0
        #             tempx5 = 0
        #
        # # skip videos (at least on youtube). Next is shift + n, and last is shift + p.
        # # hand symbol for this is all fingers down(aside from thumb). Then drag hand left to go back, and right to skip video. right now it is using short cuts...
        # # so might need to change it.
        # if (index_y > thumby) and (middle_y > thumby) and (ring_y > thumby) and (pinky_y > thumby):
        #     if (globTF == 0):
        #         tempy1 = thumby
        #         tempy2 = index_y
        #         tempy3 = middle_y
        #         tempy4 = ring_y
        #         tempy5 = pinky_y
        #         tempx1 = thumbx
        #         tempx2 = index_x
        #         tempx3 = middle_x
        #         tempx4 = ring_x
        #         tempx5 = pinky_x
        #         globTF = 1
        #     if (index_y > thumby) and (middle_y > thumby) and (ring_y > thumby) and (pinky_y > thumby):
        #         # if (index_y < thumby) and (middle_y < thumby) and (ring_y < thumby):
        #         # if (pinky_y > thumby) and (pinky_y < thumby + 10):
        #         if (thumbx < tempx1 - 100):
        #             pyautogui.keyDown('shift')
        #             pyautogui.press('p')
        #             pyautogui.keyUp('shift')
        #             globTF = 0
        #             tempy1 = 0
        #             tempy2 = 0
        #             tempy3 = 0
        #             tempy4 = 0
        #             tempy5 = 0
        #             tempx1 = 0
        #             tempx2 = 0
        #             tempx3 = 0
        #             tempx4 = 0
        #             tempx5 = 0
        #         if (thumbx > tempx1 + 100):
        #             pyautogui.keyDown('shift')
        #             pyautogui.press('n')
        #             pyautogui.keyUp('shift')
        #             globTF = 0
        #             tempy1 = 0
        #             tempy2 = 0
        #             tempy3 = 0
        #             tempy4 = 0
        #             tempy5 = 0
        #             tempx1 = 0
        #             tempx2 = 0
        #             tempx3 = 0
        #             tempx4 = 0
        #             tempx5 = 0



        #thumby is thumb, index_y is index, middle_y is middle, ring_y is ring, pinky_y is pinky
        # if (thumby > index_y) and (thumby>middle_y) and (thumby>ring_y) and (thumby>pinky_y):
        #     pyautogui.hotkey('volumemute')
        lengthfist = math.hypot(index_x - thumbx, index_y - thumby)
        # print(lengthfist)
        if (lengthfist < 50):
            x = time.perf_counter()
            print("X", x)
            if(int(x-t) == 3):
                pyautogui.hotkey('volumemute')
                t = time.perf_counter()
        if (middle_y > index_y):
            pyautogui.hotkey('volumeup')
        if (index_y > pinky_y and lengthfist > 50):
                pyautogui.hotkey('volumedown')
        #hand range 300 to 50
        # vol = np.interp(length,[50,300],[minVol,maxVol])
        # volBar = np.interp(length,[50,300],[400,150])
        # volume.SetMasterVolumeLevel(vol, None)

        if lengthfist<50:
            cv2.circle(img, (xc, yc), 15, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img,(50,150), (85,400), (0,255,0), 3)
    cv2.rectangle(img,(50,int(volBar)), (85,400), (0,255,0), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
