"""
Script to download and cache DETR models locally
Run this once to download all model files to the local cache
"""

from transformers import DetrForObjectDetection, DetrImageProcessor
import os

def download_models():
    # Create local cache directory
    cache_dir = "./models"
    os.makedirs(cache_dir, exist_ok=True)
    
    print("Downloading DETR model and processor...")
    print("This may take a few minutes depending on your internet connection.")
    
    # Download model
    print("Downloading model...")
    model = DetrForObjectDetection.from_pretrained(
        "facebook/detr-resnet-50",
        cache_dir=cache_dir
    )
    
    # Download processor
    print("Downloading processor...")
    processor = DetrImageProcessor.from_pretrained(
        "facebook/detr-resnet-50",
        cache_dir=cache_dir
    )
    
    print(f"✅ Models successfully downloaded to: {os.path.abspath(cache_dir)}")
    print("You can now run image_detection.py offline!")
    
    # Show cache contents
    print("\nCached files:")
    for root, dirs, files in os.walk(cache_dir):
        level = root.replace(cache_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_size = os.path.getsize(os.path.join(root, file))
            size_mb = file_size / (1024 * 1024)
            print(f"{subindent}{file} ({size_mb:.1f} MB)")

if __name__ == "__main__":
    download_models()
