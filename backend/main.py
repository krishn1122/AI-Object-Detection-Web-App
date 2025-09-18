from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from transformers import DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import torch
import numpy as np
import io
import base64
import os
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Object Detection API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and processor
model = None
processor = None
cache_dir = "./models"

# COCO class names
COCO_CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'N/A', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

def load_models():
    """Load DETR model and processor"""
    global model, processor
    
    try:
        logger.info("Loading DETR model and processor...")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Try to load from cache first
        if os.path.exists(cache_dir) and os.listdir(cache_dir):
            try:
                model = DetrForObjectDetection.from_pretrained(
                    "facebook/detr-resnet-50",
                    cache_dir=cache_dir,
                    local_files_only=True
                )
                processor = DetrImageProcessor.from_pretrained(
                    "facebook/detr-resnet-50",
                    cache_dir=cache_dir,
                    local_files_only=True
                )
                logger.info("✅ Models loaded from local cache")
            except:
                logger.info("Cache not found, downloading models...")
                model = DetrForObjectDetection.from_pretrained(
                    "facebook/detr-resnet-50",
                    cache_dir=cache_dir
                )
                processor = DetrImageProcessor.from_pretrained(
                    "facebook/detr-resnet-50",
                    cache_dir=cache_dir
                )
                logger.info("✅ Models downloaded and cached")
        else:
            model = DetrForObjectDetection.from_pretrained(
                "facebook/detr-resnet-50",
                cache_dir=cache_dir
            )
            processor = DetrImageProcessor.from_pretrained(
                "facebook/detr-resnet-50",
                cache_dir=cache_dir
            )
            logger.info("✅ Models downloaded and cached")
            
        model.eval()
        logger.info("Models loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        raise e

@app.on_event("startup")
async def startup_event():
    """Load models when the API starts"""
    load_models()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Object Detection API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "processor_loaded": processor is not None
    }

@app.post("/detect")
async def detect_objects(
    file: UploadFile = File(...),
    confidence_threshold: float = 0.7
):
    """
    Detect objects in an uploaded image
    
    Args:
        file: Uploaded image file
        confidence_threshold: Minimum confidence score for detections (0.0-1.0)
    
    Returns:
        JSON response with detected objects and their bounding boxes
    """
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Get image dimensions
        width, height = image.size
        
        # Preprocess the image
        inputs = processor(images=image, return_tensors="pt")
        
        # Make predictions
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Post-process results
        target_sizes = torch.tensor([image.size[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]
        
        # Filter results by confidence threshold
        detections = []
        for box, label, score in zip(results["boxes"], results["labels"], results["scores"]):
            if score > confidence_threshold:
                xmin, ymin, xmax, ymax = box.tolist()
                class_name = COCO_CLASSES[label] if label < len(COCO_CLASSES) else f"class_{label}"
                
                detections.append({
                    "class": class_name,
                    "confidence": float(score),
                    "bbox": {
                        "xmin": float(xmin),
                        "ymin": float(ymin),
                        "xmax": float(xmax),
                        "ymax": float(ymax)
                    }
                })
        
        # Convert image to base64 for frontend display
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "success": True,
            "filename": file.filename,
            "image_size": {"width": width, "height": height},
            "detections": detections,
            "total_detections": len(detections),
            "confidence_threshold": confidence_threshold,
            "image_base64": img_base64
        }
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect-batch")
async def detect_objects_batch(
    files: List[UploadFile] = File(...),
    confidence_threshold: float = 0.7
):
    """
    Detect objects in multiple uploaded images
    
    Args:
        files: List of uploaded image files
        confidence_threshold: Minimum confidence score for detections
    
    Returns:
        JSON response with results for each image
    """
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Models not loaded")
    
    results = []
    
    for file in files:
        if not file.content_type.startswith('image/'):
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "File must be an image"
            })
            continue
        
        try:
            # Process each image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            
            inputs = processor(images=image, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            target_sizes = torch.tensor([image.size[::-1]])
            detection_results = processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]
            
            # Filter and format results
            detections = []
            for box, label, score in zip(detection_results["boxes"], detection_results["labels"], detection_results["scores"]):
                if score > confidence_threshold:
                    xmin, ymin, xmax, ymax = box.tolist()
                    class_name = COCO_CLASSES[label] if label < len(COCO_CLASSES) else f"class_{label}"
                    
                    detections.append({
                        "class": class_name,
                        "confidence": float(score),
                        "bbox": {
                            "xmin": float(xmin),
                            "ymin": float(ymin),
                            "xmax": float(xmax),
                            "ymax": float(ymax)
                        }
                    })
            
            results.append({
                "filename": file.filename,
                "success": True,
                "detections": detections,
                "total_detections": len(detections)
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {
        "success": True,
        "total_images": len(files),
        "results": results,
        "confidence_threshold": confidence_threshold
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
