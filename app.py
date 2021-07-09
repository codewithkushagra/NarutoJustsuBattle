from flask import Flask,jsonify, render_template, Response
import cv2 as cv
import numpy as np
import mediapipe as mp


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)