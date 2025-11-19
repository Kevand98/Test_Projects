from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from clip_utils import get_hybrid_embedding, image_embedding
from database import images_col
import uvicorn
import os
from preprocess import index_images
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from typing import Optional

app = FastAPI(title="CLIP Image Search")

IMAGE_DIR = "/app/data/images"

# Funkar inte utan dettta
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


feature_matrix = None
image_paths = []

def load_features_into_memory():
    global feature_matrix, image_paths
    print("Loading features into memory...")
    docs = list(images_col.find({}))
    if not docs:
        print("No images found in DB.")
        return
    
    feats = []
    paths = []
    for d in docs:
        if "embedding" in d and d["embedding"]:
            feats.append(d["embedding"])
            paths.append(d["path"])
            
    if feats:
        feature_matrix = np.array(feats) # Shape: (N, 512)
        image_paths = paths
        print(f"Loaded {len(image_paths)} images into matrix.")

@app.on_event("startup")
def startup_event():
    index_images(rebuild=False) 
    load_features_into_memory()

@app.get("/")
def root():
    return {"message": "CLIP Hybrid Search API running."}

@app.post("/search")
async def search(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    top_k: int = Form(12)
):
    global feature_matrix, image_paths
    
    if feature_matrix is None or len(image_paths) == 0:
        return {"results": [], "message": "No images indexed."}

    temp_filename = None
    if file:
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as f:
            f.write(await file.read())

    if not text and not file:
        return {"error": "Provide text or image or both."}

    # 2Embedding
    try:
        query_emb = get_hybrid_embedding(text, temp_filename)
    finally:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)

    if query_emb is None:
        return {"error": "Could not generate embedding"}


    query_vec = np.array(query_emb)
    scores = feature_matrix @ query_vec 
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "path": image_paths[idx],
            "score": float(scores[idx]),
            "url": f"http://localhost:8000/image/{image_paths[idx]}"
        })

    return {"results": results}

@app.post("/index")
def trigger_index(rebuild: bool = False):
    index_images(rebuild=rebuild)
    load_features_into_memory() # Reload RAM matrix
    return {"status": "indexed", "count": len(image_paths)}

@app.get("/image/{path:path}")
def get_image(path: str):
    full = os.path.join(IMAGE_DIR, path)
    if os.path.exists(full):
        return FileResponse(full)
    return {"error": "file not found"}