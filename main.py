from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, Response
from PIL import Image
from io import BytesIO
import os
import cv2 as cv
# import desde efectos.py
from efectos import removeBackgroud, bordesColor

app = Flask(__name__)

flag_imagen_recibida = False

video_src = "video.mov"

# direccion de la webcam android obtenida desde el html
video_src_2 = "http://192.168.100.44:4747/video"

@app.route('/set_video_source', methods=['POST'])
def set_video_source():
    global video_src2
    data = request.get_json()
    address = data.get('address')
    if address:
        video_src2 = address
        return jsonify(success=True)
    return jsonify(success=False)

# en esta funcion se realiza la fusion de imagenes
def frames_video():
    global video_src_2
    video_local = cv.VideoCapture(video_src)
    video_local.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    video_local.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if video_src_2:
        video_externo = cv.VideoCapture("http://"+video_src_2+"/video")
    else:
        video_externo = None

    if not video_local.isOpened():
        print("No se pudo abrir el video")
        return
    

    while True:
        
        succes, frame = video_local.read()
        if video_externo is not None:
            succes2 , frame2 = video_externo.read()
        if not succes:
            break
        else:
            if video_externo is not None:
                # aplico efecto poner bordes
                #frame2 = bordesColor(frame2)
                # _, buffer2 = cv.imencode('.jpg', frame2)
                # frame2 = buffer2.tobytes()
                # yield (b'--frame\r\n'
                #     b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
                pass
                
            # puttext bugeado en opencv python no muestra los fps que son
            #cv.putText(frame, str(cv.CAP_PROP_FPS), (40,40), cv.FONT_HERSHEY_SIMPLEX ,1,(255, 0, 0) , 2 ,cv.LINE_AA)
           
            _, buffer = cv.imencode('.jpg', frame)
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            
            


    video_local.release()
    video_externo.release()


@app.route('/video_feed')
def video_feed():
    return Response(frames_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def frames_video_externo():
    global video_src_2
    video_ext = cv.VideoCapture(video_src_2)
    
   
    if not video_ext.isOpened():
        print("No se pudo abrir el video")
        return
    

    while True:
        
        succes2, frame2 = video_ext.read()
        
        if not succes2:
            break
        else:
            if video_ext is not None:
                # aplico efecto poner bordes
                frame2 = removeBackgroud(frame2)
                _, buffer2 = cv.imencode('.jpg', frame2)
                frame2 = buffer2.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
                

@app.route('/video_feed_externo')
def video_feed_externo():
    return Response(frames_video_externo(),
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
