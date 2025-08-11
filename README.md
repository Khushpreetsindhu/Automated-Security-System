# Automated-Security-System
This system detects and tracks human posture and if it enters a restricted zone an alarm is activated with the help of the following libraries:
1. cv2, for video and image processings.
2. time, used here for fps calculation.
3. pygame, used for playing alarm sirem.
4. threading, the alarm is played in a different thread so as not to disturb pose estimation.
It successfully detects and tracks the human body in a flow explained below.
<img width="1916" height="1001" alt="securitysystemflowchart" src="https://github.com/user-attachments/assets/17ff66f7-c351-4e7b-bc5b-426226553127" />
. System’s Camera captures the live video feed in real time.
. This feed is sent to the MediaPipe Pose Model, which processes each frame to detect human body landmarks (like joints, arms, and legs).
. The Extracted Landmarks are analyzed to check if the person has entered the restricted area.
. If landmarks are present within the restricted zone, a condition is met.
. This triggers the Alarm Activation, which alerts the user immediately via sound or other means.
