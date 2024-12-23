import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from transformers import CLIPProcessor, CLIPModel
from image_processor import decode_image
import google.auth
from google.auth.transport.requests import Request
from google.auth import jwt

app = Flask(__name__)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

CORS(app, supports_credentials=True)

# Verify the identity token
def verify_token(id_token):
    try:
        # Specify the audience for your Cloud Run service
        audience = os.environ.get('GOOGLE_CLOUD_RUN_AUDIENCE', 'https://clip-app-421314491434.europe-west3.run.app')  # Update with your Cloud Run URL
        
        # Decode and verify the token
        decoded_token = jwt.decode(id_token, audience=audience, verify=True)  # Token decoding and verification
        
        return decoded_token  # Return decoded token if verification is successful
    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        return None  # Return None if verification fails

@app.route('/run/', methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def run():
    if request.method == 'OPTIONS':
        print("options request")
        return '', 204
    
    # Extract Authorization header from the request
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Missing authorization header"}), 401
    
    token = auth_header.split("Bearer ")[-1]  # Extract token after 'Bearer '
    if not token:
        return jsonify({"error": "Invalid authorization format"}), 401
    
    # Verify the token
    decoded_token = verify_token(token)
    if not decoded_token:
        return jsonify({"error": "Unauthorized, invalid or expired token"}), 403

    # Proceed with image processing if token is valid
    data = request.json
    images = []
    images.append(decode_image(data["image"]))
    
    labels = data["labels"]

    # Pass through the model
    inputs = processor(text=labels, images=images, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # Image-text similarity score
    probabilities = logits_per_image.softmax(dim=1)  # Softmax to get label probabilities

    probabilities = probabilities.tolist()
    probs = {}
    for label_no in range(len(labels)):
        probs[labels[label_no]] = probabilities[0][label_no]
    
    # Reverse the order of key-value pairs
    final_probabilities = dict(list(probs.items())[::-1])

    response = jsonify(final_probabilities)

    print(response.data)

    return response


if __name__ == "__main__":
    app.run(port=8080, debug=True)
    # app.run(ssl_context=('ssl/server.cert', 'ssl/server.key'), port=5000, debug=True)
