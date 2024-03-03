from image_processor import encode_image
import requests
import json

def send_request(images, labels):
    req = {
        "images": [],
        "labels": []
    }
    for img in images:
        req["images"].append(encode_image(img))
    req["labels"] = labels

    response = requests.post("http://192.168.2.42:5000/", json=req)

    print(response.json())


if __name__ == "__main__":
    with open("app_emulator_config.json") as cfg_file:
        config = json.load(cfg_file)
    send_request(config["images"], config["labels"])   