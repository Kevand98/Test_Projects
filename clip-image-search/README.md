# CLIP Hybrid Image Search Engine

This project demonstrates a powerful, semantic image search engine built using OpenAI's **CLIP model** and **FastAPI**. The application allows users to search an image database based on text (e.g., "a happy dog"), an image, or a combination of both.

The entire project is containerized using Docker Compose for easy deployment and management.

## Key Features

* **Hybrid Search:** Supports Text-to-Image, Image-to-Image, and combined (Hybrid) searching for refined results.
* **Zero-Shot Learning:** The model can search for concepts it was not explicitly trained on (e.g., "a feeling of joy").
* **High Performance:** Utilizes **In-Memory Vector Search** (NumPy matrices) for near-instantaneous search results.
* **Containerized:** Easily deployable locally using Docker Compose.

## Technologies Used

* **AI Model:** CLIP (Contrastive Language–Image Pre-training)
* **Backend:** Python 3.10+ (FastAPI)
* **Vector Database (Development):** MongoDB
* **Web Server (Frontend):** Nginx
* **Containerization:** Docker & Docker Compose

## Getting Started

Follow these steps to clone the repository, load data, and start the project.

### Step 1: Data Preparation

1.  **Cloning:** Clone the repository to your local machine.
    ```bash
    git clone your-repo-url
    cd your-repo-name
    ```

2.  **Create Data Directory:** Ensure the necessary image directory exists.
    ```bash
    mkdir -p data/images
    ```

3.  **Add Images:**
    * Place all images you wish to index (JPEG, PNG, etc.) inside the `data/images` folder.
    * *For optimal testing, 50-100 high-resolution images are recommended.*

### Step 2: Build and Start Services

Run this command from the project root directory. It builds the necessary Docker images and starts all three services (frontend, backend, mongo).

```bash
docker-compose up --build -d
