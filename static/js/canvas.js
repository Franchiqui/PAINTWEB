const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    draw(e);
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.beginPath();
});

canvas.addEventListener('mousemove', draw);

function draw(e) {
    if (!drawing) return;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
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
