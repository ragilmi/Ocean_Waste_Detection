# Sea Trash Detection and Segmentation

This project was developed as part of the **Computer Vision** course at President University. It integrates object detection using **YOLOv8** and instance segmentation using **Mask R-CNN** to analyze images containing marine debris. The system identifies object locations, segments their shapes, and calculates how much of each detected object is covered by a segmentation mask.

---

## Project Members

- **Ragil Maulana Ilyasha** – 001202300117  
- **Davina Ritzky Amarina** – 001202300039  
- **Emilia Adinda Putri Ginting** – 001202300155  
- **Nava Windah Simanjuntak** – 001202300154  

---

## Repository Overview

This repository contains only the main script for running detection, segmentation, and visualization:

```

.
├── 1ocean\_waste\_setup.py

```

Other required files are stored separately on Google Drive and must be downloaded manually (see below).

---

## Required Files (Google Drive)

The following resources are essential for running the script and are available via Google Drive:

🔗 **Google Drive Folder:**  
[https://drive.google.com/drive/folders/1AuhAFc9xcNfwwSpLCR4lAP7_jw7agHFe?usp=sharing](https://drive.google.com/drive/folders/1AuhAFc9xcNfwwSpLCR4lAP7_jw7agHFe?usp=sharing)

Contents:
- `best13.pt` – YOLOv8 trained weights  
- `sea_trash_train_2.v7i.yolov8.zip` – Image dataset in YOLOv8 format

After downloading:
1. Place the `best13.pt` file in the same directory as the script.
2. Extract `sea_trash_train_2.v7i.yolov8.zip` so that the following path exists:

```

sea\_trash\_train\_2.v7i.yolov8/
└── train/
└── images/

````

---

## Installation

Ensure Python 3.8+ is installed, then install the required dependencies using:

```bash
pip install torch torchvision ultralytics matplotlib opencv-python pillow
````

---

## How to Use

Once all files are in place, run the script using:

```bash
python 1ocean_waste_setup.py
```

The script will:

* Randomly select an image from the dataset
* Perform object detection using YOLOv8
* Perform segmentation using Mask R-CNN
* Display the original image, the segmentation mask, and an overlay with bounding boxes and percentage coverage of each object

---

## Output Overview

The script displays a side-by-side comparison of:

1. The original input image
2. The generated binary segmentation mask
3. The image overlaid with segmentation and detection results, annotated with percentage coverage values

These outputs help visualize how well the segmentation overlaps with the detected object regions.

---

## License

This project is licensed under the **MIT License** and may be used freely for academic and research purposes.
