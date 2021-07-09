from flask import Flask,jsonify, render_template, Response
import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import mediapipe as mp


app = Flask(__name__)

mp_drawing=mp.solutions.drawing_utils
mp_hands= mp.solutions.hands

handsign="open"

def generate_frames():
    cap=cv.VideoCapture(0)
    detector = htm.handDetector()
    
    while cap.grab():
                
        success, frame = cap.read()  # read the camera frame
    
    
        image =cv.flip(frame, 1)
    

        image = detector.findHands(image)

        lmList0=[]
        lmList1=[]
        
        #getting hand one landmarks
        try:
            lmList0 = detector.findPosition(image,draw=False)
        except:
            pass

        #getting hand two landmarks
        try:
            lmList1 = detector.findPosition(image,draw=False,handNo=1)
        except:
            pass
        
        
        if len(lmList0) != 0:
            global handsign
            # print(f"hand 1: {lmList0}",end="\n\n\n")
            if lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]>lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                handsign="yo"
            elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]<lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                handsign="thulu"
            elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]<lmList0[20][2]:
                handsign="L"
            elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]<lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                handsign="Mid-Down"
            elif lmList0[12][2]<lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                handsign="Mid-close-Down"
            elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[7][2]<lmList0[8][2] and lmList0[19][2]<lmList0[20][2]:
                handsign="fist"
            elif lmList0[12][2]<lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]<lmList0[20][2]:
                handsign="LL"
            else:
                handsign="open"
        # if len(lmList1) != 0:
        #     print(f"hand 2: {lmList1}",end="\n\n\n")

        if not success:
            break
        else:
            ret, buffer = cv.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/video")
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/play")
def play():
    return render_template('play.html')

@app.route("/handSign")
def handSign():
    global handsign
    message = {'handsign':f'{handsign}'}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)