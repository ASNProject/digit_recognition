import requests
from flask import Flask, render_template, Response
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'capture/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0)
    while True:
        ret, frame = vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    vs.release()
    cv2.destroyAllWindows()


def save_images(image):
    filename = '1.jpg'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cv2.imwrite(filepath, image)


@app.route('/video_feed')
def video_feed():
    """Video streaming"""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def save_image_route():
    content = requests.get_data()
    nparr = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    save_images(image)
    return 'Gambar berhasil disimpan'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
