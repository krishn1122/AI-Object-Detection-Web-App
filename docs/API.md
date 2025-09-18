# API Documentation

## Overview

The Object Detection API is built with FastAPI and provides RESTful endpoints for AI-powered object detection using Facebook's DETR model.

**Base URL**: `http://localhost:8000`  
**API Documentation**: `http://localhost:8000/docs`  
**OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Authentication

Currently, the API does not require authentication. For production use, implement proper authentication mechanisms.

## Endpoints

### Health Check

#### `GET /`
Basic health check endpoint.

**Response:**
```json
{
  "message": "Object Detection API is running!",
  "status": "healthy"
}
```

#### `GET /health`
Detailed health check with model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "processor_loaded": true
}
```

### Object Detection

#### `POST /detect`
Detect objects in a single image.

**Parameters:**
- `file` (form-data): Image file (required)
- `confidence_threshold` (form-data): Float between 0.0-1.0 (default: 0.7)

**Supported formats:** PNG, JPG, JPEG, GIF, BMP, WEBP

**Example Request:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -F "file=@image.jpg" \
  -F "confidence_threshold=0.7"
```

**Response:**
```json
{
  "success": true,
  "filename": "image.jpg",
  "image_size": {
    "width": 800,
    "height": 600
  },
  "detections": [
    {
      "class": "person",
      "confidence": 0.95,
      "bbox": {
        "xmin": 100.5,
        "ymin": 50.2,
        "xmax": 300.8,
        "ymax": 400.1
      }
    }
  ],
  "total_detections": 1,
  "confidence_threshold": 0.7,
  "image_base64": "base64_encoded_image_string"
}
```

#### `POST /detect-batch`
Detect objects in multiple images.

**Parameters:**
- `files` (form-data): Multiple image files (required)
- `confidence_threshold` (form-data): Float between 0.0-1.0 (default: 0.7)

**Example Request:**
```bash
curl -X POST "http://localhost:8000/detect-batch" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "confidence_threshold=0.8"
```

**Response:**
```json
{
  "success": true,
  "total_images": 2,
  "results": [
    {
      "filename": "image1.jpg",
      "success": true,
      "detections": [...],
      "total_detections": 3
    },
    {
      "filename": "image2.jpg",
      "success": false,
      "error": "Invalid image format"
    }
  ],
  "confidence_threshold": 0.8
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "File must be an image"
}
```

### 413 Payload Too Large
```json
{
  "detail": "File too large"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "confidence_threshold"],
      "msg": "ensure this value is less than or equal to 1.0",
      "type": "value_error.number.not_le"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing image: Model not loaded"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting based on your requirements.

## CORS

CORS is enabled for all origins in development. For production, configure specific allowed origins.

## Model Information

- **Model**: Facebook DETR ResNet-50
- **Classes**: 91 COCO dataset classes
- **Input**: RGB images
- **Output**: Bounding boxes with class labels and confidence scores

### Supported Object Classes

The model can detect 91 different object classes including:
- **People**: person
- **Animals**: bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe
- **Vehicles**: bicycle, car, motorcycle, airplane, bus, train, truck, boat
- **Furniture**: chair, couch, potted plant, bed, dining table, toilet
- **Electronics**: tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator
- **Sports**: sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket
- **Food**: bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake
- **Accessories**: backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard
- **Household**: fire hydrant, stop sign, parking meter, bench, clock, vase, scissors, teddy bear, hair drier, toothbrush, book

## Performance Tips

1. **Image Size**: Smaller images process faster
2. **Batch Processing**: Use batch endpoint for multiple images
3. **Confidence Threshold**: Higher thresholds return fewer results
4. **Model Caching**: Models are cached locally after first download

## Python Client Example

```python
import requests
from pathlib import Path

# Single image detection
def detect_objects(image_path, confidence=0.7):
    url = "http://localhost:8000/detect"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'confidence_threshold': confidence}
        response = requests.post(url, files=files, data=data)
    
    return response.json()

# Usage
result = detect_objects("path/to/image.jpg", confidence=0.8)
print(f"Found {result['total_detections']} objects")
```

## JavaScript Client Example

```javascript
async function detectObjects(file, confidence = 0.7) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('confidence_threshold', confidence);
    
    const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        body: formData
    });
    
    return await response.json();
}

// Usage with file input
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    const result = await detectObjects(file, 0.8);
    console.log(`Found ${result.total_detections} objects`);
});
```
