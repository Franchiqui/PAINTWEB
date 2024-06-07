from flask import render_template, request, current_app as app
import io
from PIL import Image
import base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    image_data = request.form['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    image.save('drawing.png')
    return 'Image saved'
