from flask import Flask, render_template, request
import socket

app = Flask(__name__)

# Variable global para controlar el estado de la escucha
escuchando = False

datos_recibidos = []

# Función para recibir datos del socket
def recibir_datos():
    HOST = '0.0.0.0'  # Escucha en todas las interfaces de red
    PORT = 54321  # Puerto de escucha
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as s:
        print("socket creado")
        s.bind((HOST, PORT))
        print("socket vinculado")
        s.listen()
        print("socket escuchando ...")
        conn, addr = s.accept()
        
        print("conexion aceptada ...")
        full_data = b""
        with conn:
            print('Conexión establecida desde', addr)
            
            while escuchando:
                data = conn.recv(4096)
                if not data:
                    break

                full_data+=data
                

                print('Datos recibidos:', len(full_data),"bytes")
                

            guardar_imagen(full_data)
            print("imagen recibida!")
    s.close()  



# Función para guardar la imagen recibida
def guardar_imagen(data):
    pos = data.find(b"\r\n\r\n")
    print("header length: ",pos)
    print(data[:pos].decode())
    with open('imagen_recibida.jpg', 'wb') as f:  # Cambiar la extensión según el tipo de imagen recibida
        f.write(data)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html', datos = datos_recibidos)


# Ruta para iniciar la escucha de datos
@app.route('/iniciar_escucha', methods=['POST'])
def iniciar_escucha():
    global escuchando
    escuchando = True
    print("iniciar ")
    recibir_datos()  # Iniciar la función para recibir datos
    
    return 'Escuchando datos...'


# Ruta para detener la escucha de datos
@app.route('/detener_escucha', methods=['POST'])
def detener_escucha():
    global escuchando
    escuchando = False
    print("escucha de datos detenidad.!")
    return 'Escucha de datos detenida.'

if __name__ == '__main__':
    app.run(debug=True)
