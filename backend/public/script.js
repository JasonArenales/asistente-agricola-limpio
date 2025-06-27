// FUNCIONES PARA IMÁGENES Y ACCIONES

// Arreglo opcional para clasificaciones predefinidas (puedes expandirlo o ignorarlo)
const clasificacionesPredefinidas = [
  { label: "hoja saludable", mensaje: "🌱 La hoja parece saludable. No hay signos de plaga." },
  { label: "hoja enferma", mensaje: "⚠️ La hoja parece enferma. Revisa por plagas o deficiencias." },
  { label: "hoja seca", mensaje: "💧 La hoja está seca. Considera aumentar el riego." }
];

// Función para mostrar la imagen
function mostrarImagen(event) {
  const vista = document.getElementById("vistaPrevia");
  if (event.target.files && event.target.files[0]) {
    vista.src = URL.createObjectURL(event.target.files[0]);
    vista.classList.remove("hidden");
  } else {
    vista.classList.add("hidden");
  }
}

// Función para clasificar hoja (con opción de usar el arreglo)
function clasificarHoja() {
  const resultado = document.getElementById("resultado");
  // Simulación: podrías integrar una API o modelo aquí
  // Por ahora, usa una clasificación aleatoria del arreglo como ejemplo
  const clasificacionAleatoria = clasificacionesPredefinidas[Math.floor(Math.random() * clasificacionesPredefinidas.length)];
  resultado.innerText = clasificacionAleatoria ? clasificacionAleatoria.mensaje : "🌱 La hoja parece saludable. No hay signos de plaga.";
}

// Función para predecir salud
function predecirSalud() {
  document.getElementById("resultado").innerText = "🌿 El cultivo está en buen estado.";
}

// Función para recomendar acción
function recomendarAccion() {
  document.getElementById("resultado").innerText = "💧 Se recomienda regar hoy debido a baja humedad.";
}

// Función para hablar con el asistente
function hablarConAsistente() {
  const mensaje = "Hola agricultor, recuerda revisar tus cultivos.";
  document.getElementById("resultado").innerText = "🗣 " + mensaje;
  const speech = new SpeechSynthesisUtterance(mensaje);
  speech.lang = "es-ES";
  window.speechSynthesis.speak(speech);
}