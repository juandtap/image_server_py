// al presionar el boton se recarga la pagina mostrando la imagen recibida
document.addEventListener("DOMContentLoaded", function() {
  const reloadButton = document.getElementById("reload-button");

  reloadButton.addEventListener("click", () =>  {
      this.location.reload(); 
  });
});

function detenerVideo() {
  fetch('/stop_video')
      .then(response => {
          if (response.ok) {
              document.getElementById('video').src = "";
              console.log("se ha detenido el video");
          }
      });
}

function agregarVideo() {
  var address = document.getElementById('fuenteVideo').value;
  if (address) {
      var videoElement = document.createElement('img');
      videoElement.setAttribute('src', 'http://' + address + '/video');
      videoElement.setAttribute('width', '100%');
      videoElement.setAttribute('alt', 'Video en vivo');
      document.getElementById('videoContainer').appendChild(videoElement);
  } else {
      alert('Por favor ingresa una dirección IP y un puerto.');
  }
}
