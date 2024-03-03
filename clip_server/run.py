from flask import Flask, request, jsonify
from PIL import Image
import json
from transformers import CLIPProcessor, CLIPModel
from werkzeug.datastructures import ImmutableMultiDict

from image_processor import decode_image

app = Flask(__name__)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

@app.route('/', methods=["POST"])
def run():
    # this is what the request should look like:
    a = {
        "images": ["list of base64 strings"],
        "labels": ["list of labels"]
    }

    data = request.json

    # get image data
    images = []
    for b64 in data["images"]:
        images.append(decode_image(b64))
    
    # get label data
    labels = data["labels"]

    # pass through model
    inputs = processor(text=labels, images=images, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probabilities = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities

    probs = probabilities.tolist()

    response = {
        "probs": probs
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)