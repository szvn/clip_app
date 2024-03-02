from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

image_urls = [
    'Gottähnliches Abbild.jpeg',
    'Avatar-Beni-NPC.jpeg'
    ]
images = []
for url in image_urls:
    images.append(Image.open(url))

classes = ['son of a bitch', 'nice person']
inputs = processor(text=classes, images=images, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities