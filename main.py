from flask import Flask, request, render_template
import time
app = Flask(__name__)

TIMEOUT = 30

@app.route('/')
def index():
    return render_template('index.html', mensaje='esperando imagen ....')

@app.route('/recepcion', methods=['POST'])
def recepcion():
    time.sleep(TIMEOUT)
    if 'file' not in request.files:
        return 'No se ha enviado ningún archivo', 400

    file = request.files['file']
    if file.filename == '':
        return 'No se ha seleccionado ningún archivo', 400

    if file:
        file.save('imagen_recibida.png')  # Guardar la imagen recibida en el servidor
        return render_template('index.html', mensaje ='Imagen recibida correctamente')


if __name__ == '__main__':
    app.run(debug=True)
