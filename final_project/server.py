from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load your pre-trained model
# Ensure you have the correct path to your model
model = tf.keras.models.load_model('path_to_your_model.h5')

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def preprocess_hex_array(hex_array):
    # Convert hex array to numpy array of shape (28, 28, 1)
    image_data = [hex_to_rgb(h)[0] for h in hex_array]  # Taking the red channel (or grayscale)
    image_array = np.array(image_data).reshape((28, 28, 1))
    image_array = image_array.astype('float32') / 255.0  # Normalize to [0, 1]
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    hex_array = data['hex_data']
    if len(hex_array) != 28 * 28:
        return jsonify({'error': 'Invalid input data'}), 400
    
    # Preprocess the hex array to the correct input shape
    processed_image = preprocess_hex_array(hex_array)

    # Make prediction using the model
    prediction = model.predict(processed_image)
    
    # Assuming the model outputs a single value or class probabilities
    output = np.argmax(prediction, axis=1)[0]  # Modify based on your model's output format
    
    return jsonify({'prediction': output})

if __name__ == '__main__':
    app.run(debug=True)
