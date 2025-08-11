import cv2
import mediapipe as mp
import time



class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackingCon=0.5):

        self.mode = bool(mode)
        self.upBody = bool(upBody)
        self.smooth = bool(smooth)
        self.detectionCon = float(detectionCon)
        self.trackingCon = float(trackingCon)

        # Mediapipe setup
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose


        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,  # bool
            smooth_landmarks=self.smooth,  # bool
            min_detection_confidence=self.detectionCon,  # float
            min_tracking_confidence=self.trackingCon  # float
        )

    # Method for finding pose
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img
    #getting point positions of detected body
    def getPosition(self, img, draw=True):
        lmList = []
        if  self.results and self.results.pose_landmarks:
            h, w, c = img.shape
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                 #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
        return lmList


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()

    while True:
        success, img = cap.read()
        if not success:
            break  # break the loop if the frame is not captured properly

        img = detector.findPose(img)
        lmList = detector.getPosition(img) #use draw=False in argument
        if lmList:
            print(lmList)
        else:
            print("No lms detected")
        #highliting specific lm
        #cv2.circle(img, (lmList[16][1], lmList[16][2]), 10, (0,0,255), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  #'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
