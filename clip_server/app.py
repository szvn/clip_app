from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from transformers import CLIPProcessor, CLIPModel

from image_processor import decode_image

app = Flask(__name__)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

CORS(app, supports_credentials=True)

@app.route('/run/', methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def run():
    if request.method == 'OPTIONS':
        print("options request")
        return '', 204
    
    # this is what the request should look like:
    a = {
        "image": "list of base64 strings",
        "labels": ["list of labels"]
    }

    data = request.json

    # get image data
    images = []
    images.append(decode_image(data["image"]))
    
    # get label data
    labels = data["labels"]

    # pass through model
    inputs = processor(text=labels, images=images, return_tensors="pt", padding=True)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probabilities = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities

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