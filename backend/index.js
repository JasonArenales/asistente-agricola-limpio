const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public')); // Sirve archivos HTML desde la carpeta /public

// Ruta de ejemplo (puedes cambiarla o eliminarla)
app.post('/chat', async (req, res) => {
  res.json({ respuesta: 'Funcionalidad de OpenAI eliminada.' });
});

// Inicia el servidor
app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
