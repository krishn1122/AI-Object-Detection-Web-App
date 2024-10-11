from transformers import DetrForObjectDetection, DetrImageProcessor
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load model and processor
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model.eval()

# Load the image
image = Image.open(r"E:\\object detection\\scrub.jpg")

# Preprocess the image
inputs = processor(images=image, return_tensors="pt")

# Make predictions
with torch.no_grad():
    outputs = model(**inputs)

# Post-process results
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes)[0]


# Visualize the bounding boxes
def plot_results(image, boxes, labels):
    fig, ax = plt.subplots(1)
    ax.imshow(image)

    for box in boxes:
        xmin, ymin, xmax, ymax = box
        rect = patches.Rectangle(
            (xmin, ymin),
            xmax - xmin,
            ymax - ymin,
            linewidth=1,
            edgecolor="r",
            facecolor="none",
        )
        ax.add_patch(rect)

    plt.show()


# Show image with bounding boxes
plot_results(image, results["boxes"], results["labels"])
