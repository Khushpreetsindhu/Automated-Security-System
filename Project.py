import cv2
import time
import PoseModule as pm
import pygame
import threading

pygame.mixer.init()
#alarm thread function
alarmMode = False

def playAlarm():
    global alarmMode
    if not alarmMode:
        alarmMode = True
        pygame.mixer.music.load("alarm-siren-sound-effect.mp3")  #loading alarm
        pygame.mixer.music.play()  #playing alarm

        while pygame.mixer.music.get_busy():  #wait for the sound to finish playing
            continue

        alarmMode = False

cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.poseDetector()
#restricted zone
topLeft = (50,70)
bottomRight = (300,115)

while True:
    success, img = cap.read()
    if not success:
        break  #break loop if frame is not captured properly

    img = detector.findPose(img)
    lmList = detector.getPosition(img, draw=True)
    #drawing restricted zone
    cv2.rectangle(img, topLeft, bottomRight, (255,0,0), 2)
    #if body in restricted zone
    if lmList:
        for id,x,y in lmList:
            if topLeft[0] < x < bottomRight[0] and topLeft[1] < y < bottomRight[1]:
                cv2.putText(img, "ALARM ZONE!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Trigger alarm in a separate thread
                if not alarmMode:
                    threading.Thread(target=playAlarm, daemon=True).start()
                break  # Stop checking once any point enters the zone
    else:
        print("No lms detected")
    # highlighting specific lm
    # cv2.circle(img, (lmList[16][1], lmList[16][2]), 10, (0,0,255), cv2.FILLED)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()