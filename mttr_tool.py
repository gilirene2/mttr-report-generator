import os
import re
import quopri
from bs4 import BeautifulSoup
from dateutil import parser
import pandas as pd

def extract_created_from_file(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    decoded_content = quopri.decodestring(raw_data).decode('utf-8', errors='ignore')
    soup = BeautifulSoup(decoded_content, 'html.parser')
    plain_text = soup.get_text(separator="\n")
    lines = [line.strip() for line in plain_text.splitlines() if line.strip()]

    for i, line in enumerate(lines):
        if "Created" in line:
            for j in range(1, 4):
                if i + j < len(lines):
                    candidate = lines[i + j]
                    if re.match(r'[A-Za-z]{3,9} \d{1,2}, \d{4} \d{1,2}:\d{2} [APMapm]{2}', candidate):
                        return candidate
    return None

def extract_occurred_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    m = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', content)
    return m.group(0) if m else None

# User input for path and output
folder_path = input("Enter the folder path containing .mhtml/.html files: ").strip()
output_file = input("Enter the Excel filename to save the report (e.g. report.xlsx): ").strip()

if not os.path.exists(folder_path):
    print("Error: Folder does not exist.")
    exit()

if not output_file.lower().endswith(".xlsx"):
    output_file += ".xlsx"

records = []
for fname in os.listdir(folder_path):
    if not (fname.lower().endswith(".html") or fname.lower().endswith(".mhtml")):
        continue

    path = os.path.join(folder_path, fname)
    ticket_id = os.path.splitext(fname)[0]

    created_str  = extract_created_from_file(path)
    occurred_str = extract_occurred_from_file(path)

    if not created_str or not occurred_str:
        print(f"{ticket_id}: missing created or occurred")
        continue

    dt_created  = parser.parse(created_str).replace(tzinfo=None)
    dt_occurred = parser.parse(occurred_str).replace(tzinfo=None)

    records.append({
        "ticket_id":   ticket_id,
        "created_at":  dt_created,
        "occurred_at": dt_occurred,
    })

if not records:
    print("No valid records found.")
    exit()

df = pd.DataFrame(records)
df["mttr"]       = df["created_at"] - df["occurred_at"]
df["mttr_hours"] = df["mttr"].dt.total_seconds() / 3600

df.to_excel(output_file, index=False)
print(f"MTTR report saved as: {output_file}")
