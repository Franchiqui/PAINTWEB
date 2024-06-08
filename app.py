from flask import Flask, render_template, request, jsonify
import base64
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    image_data = request.form['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    image.save('drawing.png')
    return jsonify({"message": "Image saved"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
