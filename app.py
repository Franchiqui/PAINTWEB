from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.json
    image_data = data['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    image = ImageOps.expand(image, border=(5, 5, 5, 5), fill='white')
    image.save('static/images/saved_image.png')
    return jsonify({'message': 'Image saved successfully!'})

if __name__ == "__main__":
    app.run(debug=True)
