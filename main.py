from flask import Flask, request, render_template
from PIL import Image
from io import BytesIO
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', mensaje='esperando imagen ....')

@app.route('/recepcion', methods=['GET', 'POST'])
def recepcion():

    while request.content_type != 'image/png':
        pass

    image = request.get_data()
    with Image.open(BytesIO(image)) as img:
        img.save('imagen_recibida.png')
    return render_template('index.html', mensaje ='Imagen recibida correctamente')


if __name__ == '__main__':
    app.run(debug=True)
