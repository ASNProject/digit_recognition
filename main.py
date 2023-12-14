from flask import Flask, render_template, Response, request
import cv2
import os
import base64
from detect_image import detect_image, detect_image2, sumResult

app = Flask(__name__)
UPLOAD_FOLDER = 'capture'
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


@app.route('/video_feed')
def video_feed():
    """Video streaming"""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    image_data = data.get('image_data', '')

    # Decode data URL menjadi array byte
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    # Path untuk menyimpan gambar
    folder_path = 'capture'
    file_path = os.path.join(folder_path, '1.jpg')

    # Simpan gambar ke file
    with open(file_path, 'wb') as f:
        f.write(image_bytes)

    return 'Gambar berhasil disimpan di {}'.format(file_path)


@app.route('/save_image2', methods=['POST'])
def save_image2():
    data = request.get_json()
    image_data = data.get('image_data', '')

    # Decode data URL menjadi array byte
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    # Path untuk menyimpan gambar
    folder_path = 'capture'
    file_path = os.path.join(folder_path, '2.jpg')

    # Simpan gambar ke file
    with open(file_path, 'wb') as f:
        f.write(image_bytes)

    return 'Gambar berhasil disimpan di {}'.format(file_path)


@app.route('/detect_image', methods=['GET'])
def run_detect_image():
    detect_image()
    return detect_image()


@app.route('/detect_image2', methods=['GET'])
def run_detect_image2():
    detect_image2()
    return detect_image2()


@app.route('/result', methods=['GET'])
def result():
    sumResult()
    return sumResult()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
