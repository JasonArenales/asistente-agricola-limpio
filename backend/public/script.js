function predecirSalud() {
  document.getElementById("resultado").innerText = "🌿 El cultivo está en buen estado.";
}

function recomendarAccion() {
  document.getElementById("resultado").innerText = "💧 Se recomienda regar hoy debido a baja humedad.";
}

function hablarConAsistente() {
  const mensaje = "Hola agricultor, recuerda revisar tus cultivos.";
  document.getElementById("resultado").innerText = "🗣 " + mensaje;
  const speech = new SpeechSynthesisUtterance(mensaje);
  speech.lang = "es-ES";
  window.speechSynthesis.speak(speech);
}

//aqui es para mostrar la imagen esta función y la que sigue
function mostrarImagen(event) {
  const vista = document.getElementById("vistaPrevia");
  vista.src = URL.createObjectURL(event.target.files[0]);
  vista.classList.remove("hidden");
}

function clasificarHoja() {
  document.getElementById("resultado").innerText =
    "🌱 La hoja parece saludable. No hay signos de plaga.";
}
