// al presionar el boton se recarga la pagina mostrando la imagen recibida
document.addEventListener("DOMContentLoaded", function() {
  const reloadButton = document.getElementById("reload-button");

  reloadButton.addEventListener("click", () =>  {
      this.location.reload(); 
  });
});

// considerar borrar 
function detenerVideo() {
  fetch('/stop_video')
      .then(response => {
          if (response.ok) {
              document.getElementById('video').src = "";
              console.log("se ha detenido el video");
          }
      });
}


// ya no se usa
// function agregarVideo() {
//     var address = document.getElementById('fuenteVideo').value;
//     if (address) {
//         fetch('/set_video_source', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ address: address }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 var videoUrl = document.getElementById('get-url').getAttribute('data-url');
//                 document.getElementById('video-externo').src = videoUrl
//                 //var videoext = document.getElementById('video-externo')
//                 //videoext.setAttribute('src', videoUrl)
                
//             } else {
//                 alert('Error al establecer la fuente de video.');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });
//     } else {
//         alert('Por favor ingresa una dirección IP y un puerto.');
//     }
// }
// llama a la funcion que aplica y fusiona las imagenes
function aplicarFiltro() {
    
    fetch('/aplicar_filtro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mensaje: "Aplicar filtro" })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        
        console.log("aplicar filtro");;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// guardar por si acaso
// function agregarVideo() {
//   var address = document.getElementById('fuenteVideo').value;
//   if (address) {
//       var videoElement = document.createElement('img');
//       videoElement.setAttribute('src', 'http://' + address + '/video');
//       videoElement.setAttribute('width', '100%');
//       videoElement.setAttribute('alt', 'Video en vivo');
//       document.getElementById('videoContainer').appendChild(videoElement);
//   } else {
//       alert('Por favor ingresa una dirección IP y un puerto.');
//   }
// }