from flask import Flask, render_template, request, jsonify, send_file
import base64
import io 
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
class_names = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]

app = Flask(__name__)

model = load_model('saved_emnist_model_50_percent_data.keras')  # saved by alphanum_v3.py

@app.route('/')
def home():
    return render_template('index.html')

def numpy_to_image(array):
        """Converts a NumPy array to a grayscale image in bytes."""
        image = Image.fromarray(array.astype(np.uint8))
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

@app.route('/show-img', methods=['POST'])
def show_img():
    data_url = request.json['image']
    # Strip off the header "data:image/png;base64,"
    header, encoded = data_url.split(',', 1)
    decoded = base64.b64decode(encoded)
    img = Image.open(io.BytesIO(decoded)).convert('L')
    img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)

    arr = np.array(img_resized).astype('float32') / 255.0  # normalize to [0,1]
    arr = arr.reshape(1, 28, 28, 1)

    print("size: %s, type: %s"%(arr.shape, arr.dtype))

    data_img = (arr.squeeze()*255).astype(np.uint8)

    print("size: %s, type: %s"%(data_img.shape, data_img.dtype))

    numpy_img = Image.fromarray(data_img, mode='L')

    """
    single_image = arr[0] 
    numpy_img = Image.fromarray(single_image.astype('float32') * 255.0)  # Convert back to [0,255] range
    """

    img_io = io.BytesIO()
    numpy_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

    # using ANTIALIAS filter
    # img_resized = img.resize((28, 28), Image.ANTIALIAS) #old version of pillow
    img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)

    return jsonify({'prediction': label})

@app.route('/predict', methods=['POST'])
def predict():
    data_url = request.json['image']
    header, encoded = data_url.split(',', 1)
    decoded = base64.b64decode(encoded)
    img = Image.open(io.BytesIO(decoded)).convert('L')

    img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)

    arr = np.array(img_resized).astype('float32') / 255.0  # normalize to [0,1]

    arr = arr.reshape(1, 28, 28, 1)

    preds = model.predict(arr)
    idx = int(np.argmax(preds[0]))
    label = class_names[idx]

    return jsonify({'prediction': label})

if __name__ == '__main__':
    app.run(debug=True)
