import torch
from PIL import Image
import io


def get_yolov5(models):
    # local best.pt
    model = torch.hub.load('./yolov5', 'custom', path='./model/'+models, source='local')  # local repo
    model.conf = 0.3
    return model

def get_image_from_bytes(binary_image, max_size=720):
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image
