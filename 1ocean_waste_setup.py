import cv2
import os
import numpy as np
import torch
import matplotlib.pyplot as plt
import random
from ultralytics import YOLO
from torchvision import transforms
from PIL import Image
from torchvision.models.detection import maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights

# Paths
data_path = "/Users/agil/Downloads/sea_trash_train_2.v7i.yolov8"
train_images = os.path.join(data_path, "train", "images")

# Load YOLOv8 model
yolo_model = YOLO("/Users/agil/Downloads/sea_trash_train_2.v7i.yolov8/runs/detect/train9/weights/best13.pt")

# Load Mask R-CNN model
mask_rcnn_model = maskrcnn_resnet50_fpn(weights=MaskRCNN_ResNet50_FPN_Weights.DEFAULT)
mask_rcnn_model.eval()

# Instance Segmentation (Mask R-CNN)
def segment_objects(image_path, threshold=0.5):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.ToTensor()
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = mask_rcnn_model(image_tensor)

    masks, labels, scores = output[0]['masks'], output[0]['labels'], output[0]['scores']
    selected_masks = []
    for i in range(len(scores)):
        if scores[i] > threshold:
            mask = masks[i, 0].cpu().numpy()
            selected_masks.append(mask)
    return selected_masks

# Object Detection (YOLO)
def detect_objects(image_path, conf_threshold=0.5):
    results = yolo_model(image_path, conf=conf_threshold)
    return results

# Process Image
def process_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    # Object Detection (YOLO)
    results = detect_objects(image_path)
    
    # Instance Segmentation (Mask R-CNN)
    masks = segment_objects(image_path)
    
    # Extract detected object bounding boxes
    detected_objects = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detected_objects.append((x1, y1, x2, y2))
    
    # Plot Original Image
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(image_rgb)
    plt.title("Original Image")
    plt.axis("off")
    
    # Plot Mask
    mask_overlay = np.zeros((height, width), dtype=np.uint8)
    for mask in masks:
        mask_overlay = np.maximum(mask_overlay, (mask > 0.5).astype(np.uint8) * 255)
    
    plt.subplot(1, 3, 2)
    plt.imshow(mask_overlay, cmap='gray')
    plt.title("Mask")
    plt.axis("off")
    
    # Plot Image with Mask Overlay
    image_with_mask = image_rgb.copy()
    image_with_mask[mask_overlay > 0] = [128, 0, 128]  # Purple overlay
    
    plt.subplot(1, 3, 3)
    plt.imshow(image_with_mask)
    plt.title("Image + Mask")
    plt.axis("off")
    
    # Calculate and display segmentation coverage correctly
    for i, mask in enumerate(masks):
        
        for j, (x1, y1, x2, y2) in enumerate(detected_objects):
            # Crop the bounding box area from the mask
            object_mask = mask[y1:y2, x1:x2] > 0.5  # Boolean mask
            detected_object_area = np.sum(object_mask)  # Actual object pixels
            
            # Ensure we are only considering detected pixels, not bounding box size
            mask_coverage = (detected_object_area / np.sum(mask > 0.5)) * 100

            # Display coverage in the plot
            plt.subplot(1, 3, 3)
            plt.text(x1, y1 - 10, f"{mask_coverage:.2f}%", color='red', fontsize=12, fontweight='bold', bbox=dict(facecolor='white', alpha=0.7))
                
            print(f"Mask {i+1} covers {mask_coverage:.2f}% of detected object {j+1}")
    
    plt.show()

# Test with a random image
random_image = random.choice(os.listdir(train_images))
process_image(os.path.join(train_images, random_image))