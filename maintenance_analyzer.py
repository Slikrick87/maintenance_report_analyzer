from cost_lookup_calc import get_estimated_cost
import os
import pytesseract
from PIL import Image
import re
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# List of image files to process
# image_folder = r"C:\maintenance_reports\May2025"
# image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
records = []

image_path = "8f298421-9c47-46e8-ad24-b3ff7a7041d2.jpg"
img = Image.open(image_path)
text = pytesseract.image_to_string(img)
# Add this line after extracting text
# print(f"\n--- OCR output for {os.path.basename(image_path)} ---\n{text}\n")
month = re.search(r"Month and Year of.*?\n.*?([A-Za-z]+\s+\d{2,4})", text, re.IGNORECASE)    
vehicle = re.search(r"Vehicle Unit #.*?(\d{3,})", text, re.IGNORECASE | re.DOTALL)
mileage = re.search(r"Current Mileage.*?(\d{4,7})", text, re.IGNORECASE | re.DOTALL)
date_of_maintenance = re.search(r"Date of Maintenance\s*\n(\w+ \d+)", text)
description = re.search(r"Specific Description of Maintenance Performed\s*\n(.+)", text)
date_completed = re.search(r"Date Completed\s*\n(\d{2}/\d{2}/\d{2})", text)
maintenance_entries = re.findall(r"\|\s*([A-Za-z]+\s+\d{1,2})\s*\|?\s*(.+)", text)

for entry in maintenance_entries:
    date_completed, description = entry
    record = {
        "Month": month.group(1) if month else None,
        "Vehicle": vehicle.group(1) if vehicle else None,
        "Mileage": int(mileage.group(1)) if mileage else None,
        "Maintenance Date": None,  # Not used in this case
        "Description": description.strip(),
        "Date Completed": date_completed.strip(),
        "Estimated Cost": get_estimated_cost(description)
    }
    records.append(record)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(records)
print(df)