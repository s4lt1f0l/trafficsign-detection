# Project Overview: TrafficSign Recognition

This project is a Deep Learning application focused on detecting and classifying traffic signs. It supports multiple architectures including YOLOv8, Faster R-CNN, and DETR. The project includes a Jupyter notebook for training and a Streamlit-based web application for real-time inference.

## Tech Stack
- **Deep Learning Frameworks:** PyTorch, Ultralytics (YOLOv8), Transformers (DETR).
- **Data Handling:** OpenCV, NumPy, Pillow, Pandas.
- **Web Interface:** Streamlit.
- **Visualization:** Matplotlib, Supervision.

## Directory Structure
- `models/`: Contains data loading logic (e.g., `dataset.py`).
- `web/`: Contains the Streamlit web application (`app.py`).
- `weights/`: Stores pre-trained model weights (`.pt`, `.pth`, and `best_detr_model/`).
- `labck-htk.ipynb`: Main Jupyter notebook for experiments and training.
- `requirements.txt`: Python dependencies.

## Building and Running

### 1. Environment Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Running the Web App
To start the Traffic Sign Recognition web interface:
```bash
streamlit run web/app.py
```

### 3. Training/Experiments
Open `labck-htk.ipynb` in a Jupyter environment to view or run training experiments.

## Development Conventions
- **Model Standard:**
  - YOLO: Uses `ultralytics` format.
  - DETR: Normalizes labels to 0-4 and coordinates to `[cx, cy, w, h]` (0-1).
  - R-CNN: Uses labels 1-5 and pixel coordinates `[xmin, ymin, xmax, ymax]`.
- **Dataset Loading:** Use `models.dataset.TrafficSignDataset` which handles different coordinate formats based on the `model_type` parameter.
- **Weights:** Always place pre-trained weights in the `weights/` directory.
