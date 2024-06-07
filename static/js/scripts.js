let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let drawing = false;
let brushSize = 5;
let selectedColor = 'black';

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

function startDrawing(event) {
    drawing = true;
    draw(event);
}

function draw(event) {
    if (!drawing) return;
    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.strokeStyle = selectedColor;

    ctx.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function saveImage() {
    let image = canvas.toDataURL();
    fetch('/save_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: image }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
