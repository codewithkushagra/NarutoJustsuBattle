from flask import Flask,jsonify, render_template, Response,request
import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import mediapipe as mp
import json

app = Flask(__name__)

mp_drawing=mp.solutions.drawing_utils
mp_hands= mp.solutions.hands

handsign="no move"
handsign0="no move"
currentjutsu="none"


def generate_frames(videoindex):
    
    cap=cv.VideoCapture(videoindex)
    
    detector = htm.handDetector()
    
    while cap.grab():
                
        success, frame = cap.read()  # read the camera frame
    
    
        image =cv.flip(frame, 1)
        
        global currentjutsu
        global handsign
        
        if currentjutsu=="none":
            if videoindex==0:
                image = detector.findHands(image)


                lmList0=[]
                
                #getting hand one landmarks
                try:
                    lmList0 = detector.findPosition(image,draw=False)
                except:
                    pass

                
                
                if len(lmList0) != 0:
                    
                    # print(f"hand 1: {lmList0}",end="\n\n\n")
                    
                    if lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                        handsign="yo"
                    elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]<lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                        handsign="thulu"
                    elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]<lmList0[20][2]:
                        handsign="L"
                    elif lmList0[12][2]<lmList0[11][2] and lmList0[16][2]<lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                        handsign="open"
                    elif lmList0[12][2]>lmList0[11][2] and lmList0[16][2]<lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                        handsign="MidDown"
                    elif lmList0[12][2]<lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]>lmList0[20][2]:
                        handsign="MidcloseDown"
                    elif lmList0[12][2]>lmList0[11][2] and lmList0[4][1]>lmList0[5][1] and lmList0[16][2]>lmList0[15][2] and lmList0[7][2]<lmList0[8][2] and lmList0[19][2]<lmList0[20][2]:
                        handsign="fist"
                    elif lmList0[12][2]<lmList0[11][2] and lmList0[16][2]>lmList0[15][2] and lmList0[4][1]<lmList0[5][1] and lmList0[7][2]>lmList0[8][2] and lmList0[19][2]<lmList0[20][2]:
                        handsign="LL"
                    else:
                        handsign="no move"
            


        else:
            if currentjutsu=="firebon":
                image[:,:,1],image[:,:,0]=0,0
            elif currentjutsu=="amaterasu":
                image, dst_color = cv.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
       
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
    return Response(generate_frames(0),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/video0")
def video0():
    return Response(generate_frames(2),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/play")
def play():
    return render_template('play.html')


@app.route("/jutsumade",methods=["GET", "POST"])
def jutsumade():
    global currentjutsu
    global handsign
    if request.method=='POST':
        currentjutsu=request.data
        currentjutsu=currentjutsu.decode('ASCII')
        currentjutsu=json.loads(currentjutsu)
        currentjutsu=currentjutsu['jutsu']
    
    handsign="no move"
    message = {'jutsuname':f'{currentjutsu}'}
    
    return jsonify(message)     


@app.route("/handSign")
def handSign():
    global handsign
    message = {'handsign':f'{handsign}','handsign0':f'{handsign0}'}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)