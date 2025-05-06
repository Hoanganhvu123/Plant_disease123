import os
import random # Added random import
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory, url_for, send_file
from PIL import Image
# Re-enable torch/torchvision imports
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
# import chatbot  # Comment out chatbot module

disease_info = pd.read_csv('disease_info.csv', encoding='utf-8')
# supplement_info = pd.read_csv('supplement_info.csv',encoding='cp1252') # Commented out as not used

# --- Model Loading (Re-enabled) ---
model_loaded = False
model = None # Initialize model variable
MODEL_PATH = "plant_disease_model_1_latest.pt"
try:
    if os.path.exists(MODEL_PATH):
        print(f"Attempting to load model from: {os.path.abspath(MODEL_PATH)}")
        model = CNN.CNN(39) # Assuming 39 classes based on previous context
        # Load the model state dict, mapping to CPU explicitly
        model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
        model.eval() # Set model to evaluation mode
        model_loaded = True
        print("Model loaded successfully.")
    else:
         print(f"ERROR: Model file not found at {os.path.abspath(MODEL_PATH)}")
         print("Please ensure the model file exists in the 'Flask Deployed App' directory.")
         model_loaded = False
except ImportError as e:
    print(f"ERROR loading model dependencies (torch/CNN?): {e}")
    model_loaded = False
except FileNotFoundError:
    print(f"ERROR: Model file '{MODEL_PATH}' not found.")
    model_loaded = False
except Exception as e:
    print(f"An error occurred loading the model: {e}")
    model_loaded = False
# --- End Model Loading ---


# --- Mock Prediction Function (Keep for fallback/testing if needed) ---
def prediction(image_path):
    """Returns a random disease index and a mock confidence score."""
    try:
        num_diseases = len(disease_info)
        if num_diseases == 0:
            return -1, "Disease info CSV is empty"

        # Pick a random disease index (excluding index 4 - Background Without Leaves if present)
        # Ensure the random index is valid
        possible_indices = [i for i in range(num_diseases) if i != 4]
        if not possible_indices:
             return -1, "No valid disease indices found (excluding potential background class)"

        random_index = random.choice(possible_indices)
        mock_confidence = random.uniform(0.65, 0.98) # Generate random confidence between 65% and 98%
        print(f"Mock Prediction: Index={random_index}, Confidence={mock_confidence:.2f}")
        return random_index, mock_confidence
    except Exception as e:
        print(f"Error during mock prediction: {e}")
        return -1, str(e)
# --- End Mock Prediction Function ---

# --- Real Prediction Function (Enabled) ---
def prediction_real(image_path):
    if not model_loaded:
        return -1, "Model not loaded"
    try:
        image = Image.open(image_path).convert('RGB')
        image = image.resize((224, 224))
        input_data = TF.to_tensor(image)
        input_data = input_data.view((-1, 3, 224, 224))
        output = model(input_data)
        probabilities = torch.softmax(output, dim=1)
        confidence, pred_index = torch.max(probabilities, 1)
        # Convert tensor to Python numbers
        pred_index_item = pred_index.item()
        confidence_item = confidence.item()
        print(f"Real Prediction: Index={pred_index_item}, Confidence={confidence_item:.4f}")
        return pred_index_item, confidence_item
    except Exception as e:
        print(f"Error during real prediction: {e}")
        return -1, str(e)
# --- End Real Prediction Function ---


app = Flask(__name__,
            static_folder="static",
            static_url_path='/static')

# Removed old template rendering routes as they are handled by the frontend now
# @app.route('/')
# def home_page():
#     return render_template('home.html')
#
# @app.route('/contact')
# def contact():
#     return render_template('contact-us.html')
#
# @app.route('/index')
# def ai_engine_page():
#     return render_template('index.html')

@app.route('/')
def index():
    return send_from_directory(app.root_path, 'index.html')

# --- API Endpoint for Image Submission (Original - Currently Mocked, Keep for reference or future real model use) ---
@app.route('/submit', methods=['POST'])
def submit():
    # For now, this endpoint might return an error or a simple message
    # indicating to use /api/test for mock predictions.
    # Or you could revert it to use the commented-out real prediction logic.
    print("Accessed /submit endpoint (currently inactive for mock testing)")
    return jsonify({"message": "This endpoint is currently set up for the real model (which is disabled due to memory issues). Use /api/test for mock predictions.", "success": False}), 501 # Not Implemented or custom code


# --- NEW API Endpoint for Mock Testing --- Should now use real model
@app.route('/api/test', methods=['POST'])
def test_submit_real(): # Renamed for clarity
    """Handles image upload and returns REAL prediction data."""
    if not model_loaded: # Check if model loaded successfully
         print("Model not loaded, cannot process request.")
         return jsonify({"error": "Model chưa được tải thành công, không thể xử lý yêu cầu."}), 503 # Service Unavailable

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = image.filename # Use secure_filename in production
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)

    try:
        image.save(file_path)
        print(f"Image saved for real test: {file_path}")
    except Exception as e:
         print(f"Error saving file for real test: {e}")
         return jsonify({"error": f"Error saving uploaded file: {e}"}), 500

    # Use the REAL prediction function
    pred_index, confidence = prediction_real(file_path)

    if pred_index == -1:
        error_message = confidence # Confidence variable holds the error message here
        print(f"Real Prediction error: {error_message}")
        return jsonify({"error": f"Lỗi khi xử lý ảnh bằng model: {error_message}"}), 500

    # Fetch info based on prediction index
    try:
        if not 0 <= pred_index < len(disease_info):
             return jsonify({"error": f"Mock prediction index {pred_index} out of bounds."}), 500

        title = disease_info['disease_name'][pred_index]
        description = disease_info['description'][pred_index]
        prevent = disease_info['Possible Steps'][pred_index]
        image_url = url_for('static', filename=f'uploads/{filename}')

        return jsonify({
            "success": True,
            "prediction": {
                "index": int(pred_index),
                "title": title,
                "description": description,
                "prevent": prevent,
                "confidence": round(confidence * 100, 2),
                "image_url": image_url
            }
        })
    except KeyError as e:
         return jsonify({"error": f"Invalid key in disease info for index {pred_index}: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error fetching disease info: {e}"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint for chatbot interactions"""
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
    
    prompt = data['prompt']
    
    # Tạm thời trả về phản hồi mặc định vì chatbot đã bị tắt
    response_text = "Chức năng chatbot hiện không khả dụng. Vui lòng thử lại sau."
    
    return jsonify({
        "response": response_text
    })

@app.route('/api/chatbot/suggestions', methods=['POST'])
def get_suggestions():
    """Get suggested responses for the chatbot"""
    data = request.json
    if not data or 'disease_name' not in data:
        return jsonify({"error": "No disease name provided"}), 400
    
    disease_name = data['disease_name']
    
    # Trả về các gợi ý mặc định thay vì sử dụng module chatbot
    suggestions = [
        f"Làm thế nào để điều trị bệnh {disease_name}?",
        f"Làm cách nào để phòng ngừa bệnh {disease_name}?", 
        f"Bệnh {disease_name} có lây lan không?",
        "Làm thế nào để nhận biết sớm bệnh này?"
    ]
    
    return jsonify({
        "suggestions": suggestions
    })

@app.route('/.env', methods=['GET'])
def forbidden():
    """Block access to .env file"""
    return jsonify({"error": "Access forbidden"}), 403

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files or return 404"""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return "File not found", 404

if __name__ == '__main__':
    if model_loaded:
      print("Starting Flask app with REAL model loaded.")
    else:
        print("Starting Flask app FAILED TO LOAD REAL MODEL. API /api/test will return errors.")
    # Make sure host='0.0.0.0' if you need to access it from other devices on your network
    app.run(debug=False, host='0.0.0.0', port=5000) # Specify host and port
