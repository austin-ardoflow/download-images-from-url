# download-images-from-url
## Instructions

### 1. Set Up a Python Virtual Environment

Open a terminal in the project directory and run:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies

Install required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Prepare the CSV File

Ensure your CSV file (with product links and UPCs) is in the project directory and named as "products.xlsx". The expected format is one row per image, with columns for the image URL and the corresponding UPC.

### 4. Run the Script

Execute the script:
```bash
python save_images.py
```
The script will read the CSV file (ensure the filename matches what is expected in the script, e.g., `input.csv`), download each image, and save it as a JPEG named with the UPC and `_B` suffix in the output folder.

### 5. Zip the Images Folder

After completion, compress the output folder containing the images and share as needed.

---

## Repository File Overview

| File/Folder         | Description                                                        |
|---------------------|--------------------------------------------------------------------|
| `save_images.py`    | Python script to download images from URLs and save them as JPEGs. |
| `requirements.txt`  | Lists Python dependencies required to run the script.              |
| `README.md`         | Project documentation and usage instructions.                      |