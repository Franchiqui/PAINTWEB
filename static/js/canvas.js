const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let brushSize = 2;
let selectedColor = 'black';

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    draw(e);
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.beginPath();
});

canvas.addEventListener('mousemove', draw);

document.getElementById('brushSize').addEventListener('input', (e) => {
    brushSize = e.target.value;
});

document.getElementById('brushColor').addEventListener('input', (e) => {
    selectedColor = e.target.value;
});

function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = selectedColor;

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function selectBrush() {
    selectedColor = document.getElementById('brushColor').value;
}

function selectEraser() {
    selectedColor = '#FFFFFF';
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function saveDrawing() {
    const dataURL = canvas.toDataURL();
    fetch('/save_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'image=' + encodeURIComponent(dataURL),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}

function addText() {
    const text = document.getElementById('textInput').value;
    const font = document.getElementById('fontSelect').value;
    const size = brushSize;
    const x = canvas.width / 2;
    const y = canvas.height / 2;

    ctx.font = size + 'px ' + font;
    ctx.fillStyle = selectedColor;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, x, y);
}

// Variables globales para las herramientas y colores
let currentTool = 'brush';
let strokeColor = '#000000';
let fillColor = '#ffffff';

// Funciones para seleccionar herramientas y colores
function selectBrush() {
    currentTool = 'brush';
}

function selectEraser() {
    currentTool = 'eraser';
}

function selectLine() {
    currentTool = 'line';
}

function selectCurve() {
    currentTool = 'curve';
}

function selectRectangle() {
    currentTool = 'rectangle';
}

function selectCircle() {
    currentTool = 'circle';
}

function changeStrokeColor() {
    strokeColor = document.getElementById('strokeColor').value;
}

function changeFillColor() {
    fillColor = document.getElementById('fillColor').value;
}


