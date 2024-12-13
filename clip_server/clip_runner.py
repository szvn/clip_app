from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
import datetime

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

image_urls = [
    'clip_server/img/Gottaehnliches_Abbild.jpeg',
    'clip_server/img/Avatar-Beni-NPC.JPEG'
    ]
images = []
for url in image_urls:
    images.append(Image.open(url))

classes = ['son of a bitch', 'nice person']

start_1 = datetime.datetime.now()
inputs = processor(text=classes, images=images, return_tensors="pt", padding=True)
end_1 = datetime.datetime.now()
print(f"Input processing: {end_1-start_1}")

start_2 = datetime.datetime.now()
outputs = model(**inputs)
end_2 = datetime.datetime.now()
print(f"Inference: {end_2-start_2}")

start_3 = datetime.datetime.now()
logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1)  # we can take the softmax to get the label probabilities
end_3 = datetime.datetime.now()
print(f"Output processing: {end_3-start_3}")