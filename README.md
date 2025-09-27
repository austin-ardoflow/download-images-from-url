# download-images-from-url
[Download & Rename 185 Product Photos](https://www.freelancer.com/projects/scripting/Download-Rename-Product-Photos/details)


## Project Details

I have a CSV that lists 185 product links, each paired with its UPC. Your job is simple: pull every image, keep it in its original resolution, and save it as a JPEG whose filename is exactly the UPC shown beside the link with an additional _B, for example the first image in the list should be named 725125008396_B. All images can live together in one folder; no sub-directories are needed. When you finish, zip the folder and return it or upload a Dropbox link. If you automate the task with Python, PowerShell, or any other tool, please include the script so I can reproduce the process later if the list grows.  That’s it—clean, organized, and ready for bulk import on my end.

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