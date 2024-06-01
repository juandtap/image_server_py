from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for, Response
from PIL import Image
from io import BytesIO
import os
import cv2 as cv
import numpy as np
# import desde efectos.py
from efectos import removeBackgroud, bordesColor

app = Flask(__name__)

flag_imagen_recibida = False

# origenes para fusionar la imagen
# el video tiene una resolcion de 1920x1080
# la imagen se copia en el punto (1600, 500) 
x_img_o = 1600
y_img_o = 500
# el video de la fuente 2 se copia en (100, 400) 
x_vid_o = 100
y_vid_o = 400

video_src = "video.mov"

# direccion de la webcam
video_src_2 = "172.16.213.103:4747"

# obtienne la ip de la webcam al presionar el boton "obtener video"
@app.route('/set_video_source', methods=['POST'])
def set_video_source():
    global video_src_2
    data = request.get_json()
    address = data.get('address')
    if address:
        video_src_2 = address
        return jsonify(success=True)
    return jsonify(success=False)

# en esta funcion se realiza la fusion de imagenes
def frames_video():
    
    video_local = cv.VideoCapture(video_src)
    
    if not video_local.isOpened():
        print("No se pudo abrir el video local")
        return


    while True:
        
        succes, frame = video_local.read()
       
        if not succes:
            break
        else:
            
            #cv.putText(frame, str(cv.CAP_PROP_FPS), (40,40), cv.FONT_HERSHEY_SIMPLEX ,1,(255, 0, 0) , 2 ,cv.LINE_AA)          
            _, buffer = cv.imencode('.jpg', frame)
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            
    video_local.release()
    

@app.route('/video_feed')
def video_feed():
    return Response(frames_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ya no se usa, la fusion se la hace directamente en el metodo aplicar_filtros 
# solo se puede acceder a la camara una solicitud a la vez, buscar otra forma o app 
def frames_video_externo():
    global video_src_2
    print(video_src_2)
    video_ext = cv.VideoCapture("http://"+video_src_2+"/video")
    
   
    if not video_ext.isOpened():
        print("No se pudo abrir el video externo")
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


# funcion aplicar filtro

@app.route('/aplicar_filtro', methods=['POST'])
def aplicar_filtro():
    
    data = request.json
    print(data)
    
    imagen_android = cv.imread('static/Images/imagen_recibida.png')

    ancho_img = imagen_android.shape[1]
    alto_img = imagen_android.shape[0]
    
    video_local = cv.VideoCapture("video.mov")

    if video_local.isOpened():

        video_externo = cv.VideoCapture("http://"+video_src_2+"/video")

        if video_externo.isOpened():
            print("abrio video ", video_src_2)
        else:
            print("NO se abrio el video ", video_src_2)

        while True:
            
            _, frame = video_local.read()

            _, frame2 = video_externo.read()

            frame_sin_fondo = removeBackgroud(frame2)

            frame_bordes = bordesColor(frame_sin_fondo)

            resultado_final = cv.addWeighted(frame_sin_fondo, 1, frame_bordes, 1, 0)

            # la imagen recibida desde android no tiene fondo por lo que los piexles vacios se ven en color 
            # negro por lo que quitamos los pixeles negros (0,0,0)

            # usamos la mascara para copiar solo los pixeles no negros
            mask = np.any(imagen_android != [0, 0, 0], axis=-1)
        
            # convertimos la mascara a color 
            mask_rgb = np.stack([mask, mask, mask], axis=-1)
        
            # copiamos todos los pixeles no negros(vacios) al video
            frame[y_img_o:y_img_o + alto_img, x_img_o:x_img_o + ancho_img][mask_rgb] = imagen_android[mask_rgb]
            
            # se hace el mismo proceso para el video externo, solo que ahora se quita los pixels en blanco
            mask2 = np.any(resultado_final != [255,255,255], axis=-1)
            mask_rgb2 = np.stack([mask2,mask2,mask2], axis=-1)


            frame[y_vid_o:y_vid_o+frame2.shape[0], x_vid_o:x_vid_o+frame2.shape[1]][mask_rgb2] = resultado_final[mask_rgb2]

            cv.imshow("final", frame)

            if cv.waitKey(1) == ord('q'):
                break

    
    
    
    return jsonify({'status': 'Filtro aplicado'})

# funcion para detener el video # aun no se a usado
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
    # solo para retornar algo
    return  jsonify({'mensaje': 'imagen recibida'})



@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)



if __name__ == '__main__':
   
    app.run(debug=True, host="0.0.0.0")
