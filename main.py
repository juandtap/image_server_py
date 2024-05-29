from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, Response
from PIL import Image
from io import BytesIO
import os
import cv2 as cv

app = Flask(__name__)

flag_imagen_recibida = False

video_src = "video.mov"


def frames_video():
    video_local = cv.VideoCapture(video_src)
    video_local.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    video_local.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    if not video_local.isOpened():
        print("No se pudo abrir el video")
        return
    
    


    while True:
        
        succes, frame = video_local.read()
        if not succes:
            break
        else:

            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    video_local.release()


@app.route('/video_feed')
def video_feed():
    return Response(frames_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# funcion para detener el video
@app.route('/stop_video')
def stop_video():
    return redirect(url_for('index'))

@app.route('/')
def index():
    global flag_imagen_recibida
    if flag_imagen_recibida:
        image_src = "static/Images/imagen_recibida.png"
        mensaje = "Imagen recibida correctamente"
    else:
        image_src = None
        mensaje = "Esperando imagen..."

    return render_template('index.html', mensaje=mensaje, image_src=image_src)

# Funcion para recibir la imagen, se llama desde la app android
@app.route('/recepcion', methods=['GET','POST'])
def recepcion():
    global flag_imagen_recibida

    if request.content_type == 'image/png':
        image = request.get_data()
        
        image_path = 'static/Images/imagen_recibida.png'
        with Image.open(BytesIO(image)) as img:
            img.save(image_path)
        flag_imagen_recibida = True
        print("imagen recibida")
    # solo se muestra en curl 
    return  jsonify({'mensaje': 'imagen recibida'})



@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)



if __name__ == '__main__':
   
    app.run(debug=True, host="0.0.0.0")
