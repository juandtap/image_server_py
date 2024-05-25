// al presionar el boton se recarga la pagina mostrando la imagen recibida
document.addEventListener("DOMContentLoaded", function() {
  const reloadButton = document.getElementById("reload-button");

  reloadButton.addEventListener("click", () =>  {
      this.location.reload(); 
  });
});
