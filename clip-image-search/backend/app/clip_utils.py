from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_NAME = "openai/clip-vit-base-patch32"

_model = None
_processor = None

def get_model():
    global _model, _processor
    if _model is None or _processor is None:
        _model = CLIPModel.from_pretrained(MODEL_NAME).to(device)
        _processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    return _model, _processor

def normalize(emb):
    return emb / np.linalg.norm(emb)

def image_embedding(image_path):
    model, processor = get_model()
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        emb = model.get_image_features(**inputs)
    emb = emb.cpu().numpy()[0]
    return normalize(emb).tolist()

def text_embedding(text):
    model, processor = get_model()
    inputs = processor(text=[text], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        emb = model.get_text_features(**inputs)
    emb = emb.cpu().numpy()[0]
    return normalize(emb).tolist()

def get_hybrid_embedding(text=None, image_path=None):
    emb_text = text_embedding(text) if text else None
    emb_img = image_embedding(image_path) if image_path else None

    if emb_text is not None and emb_img is not None:
        combined = (np.array(emb_text) + np.array(emb_img)) / 2.0
        return normalize(combined).tolist()
    elif emb_text is not None:
        return emb_text
    elif emb_img is not None:
        return emb_img
    else:
        return None