"""Extract EXIF datetime from JPG images and save to CSV.

Change the folder path, padding, format, selection as needed.

"""

from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

folder = r"\\klient.uib.no\\FELLES\LAB-IT\\IFT\\resfys\\FluidFlower\\FF glass beads\\050825_glass_beads_1_150_s"
pad = 5
format = "*.JPG"
files = sorted(Path(folder).glob(format))
output_csv = "image_dates.csv"

# Example selection: first 10 and then every 100th file - or all images.
# selection = files[:10] + files[10::100]
selection = files

# Initialize lists to store data
file_paths = []
file_ids = []
date_times = []

# Process each file
for i, filename in enumerate(selection):
    logging.info(f"Processing file {i} / {len(selection)}")
    file_path = filename.name
    file_id = Path(filename).stem[-pad:]
    with Image.open(filename) as img:
        exif_data = img._getexif()
        if exif_data:
            # Find DateTimeOriginal or DateTime
            date_str = None
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag in ["DateTimeOriginal", "DateTime"]:
                    date_str = value
                    break
            if date_str:
                date_time = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            else:
                date_time = None
                logger.warning(f"{file_id}: No EXIF datetime found.")
        else:
            date_time = None
            logger.warning(f"{file_id}: No EXIF data found.")
    logger.info(f"{file_id}: {date_time}")
    file_paths.append(file_path)
    file_ids.append(file_id)
    date_times.append(date_time)

# Create a DataFrame and save to CSV
df = pd.DataFrame({"path": file_paths, "image_id": file_ids, "datetime": date_times})
df.to_csv(output_csv, index=False)
