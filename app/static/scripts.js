let canvas = document.getElementById('drawingCanvas');
let context = canvas.getContext('2d');
let isDrawing = false;

canvas.addEventListener('mousedown', () => { isDrawing = true });
canvas.addEventListener('mouseup', () => { isDrawing = false; context.beginPath() });
canvas.addEventListener('mousemove', draw);

function draw(event) {
    if (!isDrawing) return;
    context.lineWidth = 2;
    context.lineCap = 'round';
    context.strokeStyle = 'black';

    context.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
    context.stroke();
    context.beginPath();
    context.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
}

function saveImage() {
    let imageData = canvas.toDataURL('image/png');
    fetch('/save_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'image=' + encodeURIComponent(imageData)
    }).then(response => response.text()).then(result => {
        alert(result);
    });
}
