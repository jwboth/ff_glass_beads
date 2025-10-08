"""Example script to copy selected images from a network drive to a local directory.

Change the source and destination paths as needed.

"""

import os
import shutil

# Define the source and destination directories
source_dir = r"\\klient.uib.no\\FELLES\LAB-IT\\IFT\\resfys\\FluidFlower\\FF glass beads\\050825_glass_beads_1_150_s"
destination_dir = "E:\\fluidflower_glass_beads"

# Create destination folder if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# List all files in the source directory
all_files = sorted(os.listdir(source_dir))

# Filter image files (assuming they are .jpg, .png, or .tif)
image_files = [
    f
    for f in all_files
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".tif", ".tiff"))
]

# Sort images by filename
image_files.sort()

# Select first 10 and then every 50th image
selected_files = image_files[:10] + image_files[10::100]
print(f"Total images found: {len(selected_files)}")

# Copy selected files to destination
for filename in selected_files:
    src_path = os.path.join(source_dir, filename)
    dst_path = os.path.join(destination_dir, filename)
    shutil.copy2(src_path, dst_path)
