import os
from database import images_col
from clip_utils import image_embedding
from tqdm import tqdm

IMAGE_DIR = "/app/data/images"

def index_images(rebuild=False):
    paths = []
    for root, dirs, files in os.walk(IMAGE_DIR):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, IMAGE_DIR)
                paths.append((rel, full))
    print(f"Found {len(paths)} images to index.")
    for rel, full in tqdm(paths):
        doc = images_col.find_one({"path": rel})
        if doc and not rebuild:
            continue
        emb = image_embedding(full)
        metadata = {
            "path": rel,
            "embedding": emb,
        }
        images_col.update_one({"path": rel}, {"$set": metadata}, upsert=True)
    print("Indexing complete.")

if __name__ == "__main__":
    index_images()
