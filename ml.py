import torch
import numpy as np
from PIL import Image
import os

def process_file(app, filename, confidence):
    DEVICE = 'cpu'
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.to(DEVICE)
    model.eval()

    model.conf = confidence

    filepath = os.path.join(app.config['IMG_UPLOAD_FOLDER'], filename)
    img = get_downsized_image(app, filepath)

    with torch.no_grad():
        results = model(img)

    out_filename = filename.split('.')[0] + '.jpg'
    results.files[0] = out_filename
    results.save(app.config['IMG_OUTPUT_FOLDER'])
    return out_filename

def get_downsized_image(app, filepath):
    img = Image.open(filepath)
    img.thumbnail(app.config['IMG_DOWNSIZE_TO'])
    img = np.array(img)
    return img
