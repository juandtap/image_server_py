## Proyecto Integrador

## Vision por computador P64

### Autor: Diego Tapia, Paul Astudillo (https://github.com/Paul-Astudillo)

Servidor Flask para fusion de imagenes provenientes desde dos fuentes, la primera la computadora desde donde se ejecuta este servidor y la segunda desde la apliaccion en Android la cual envia la imagen procesada por sockets.

### Funcionamiento

Para mayor comodidad la webcam debe estar ya activa, y la imagen tambien enviada desde android antes de abrir

### Metodo para recibir imagenes
Desde la app de android se envia la imagen por http al endpoint http://servidorflask:5000/recepcion
En la app de android se especifica la direccion IP del servidor flask

### Fuentes de video
Se tiene dos fuentes de videos, un video .mov local en la raiz del proyecto, ignorado por git ( > 400Mb). 
La segunda fuente de video es la camara de un telefono android, usado como webcam con la aplicacion DroidCam.

El frontend pide la direccion IP de la "webcam"

### Fusion 
La imagen recibida desde android y el video externo con efectos, son "fusionados" con el video.

### Efectos

Se tienen los siguientes efectos:

App Android:
    - Fusion con textura de fuego
    - Quitar fondo usando el espacio de colores LAB

Servidor Flask:
    - Quitar fondo
    - Deteccion de bordes (Canny, Dilaacion, GaussianBlur)
    







