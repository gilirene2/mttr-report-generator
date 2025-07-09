# 🛠️ MTTR Report Generator for HTML Ticket Exports

This script calculates **Mean Time to Resolution (MTTR)** by extracting "Occurred" and "Created" timestamps from `.html` or `.mhtml` files — such as incident ticket exports from platforms like Arctic Wolf.

---

## 💡 Why This Exists

Arctic Wolf's ticketing portal allows exporting tickets as **"Webpage, complete (.html)"** files. These files use a complex structure with encoded characters (quoted-printable encoding) and hidden timestamps inside HTML elements. Manually parsing these files to get time-based metrics like MTTR is tedious and error-prone.

This tool automates that process by:
- Decoding the ticket file
- Parsing and identifying timestamps
- Calculating the time difference between when an incident occurred and when it was created
- Exporting the data to Excel

---

## ⚙️ How It Works

✅ Key functions:
- `extract_created_from_file()`: Extracts the "Created" timestamp, found near the visible "Created" label in the decoded HTML
- `extract_occurred_from_file()`: Extracts the ISO-style UTC "Occurred" timestamp (e.g., `2025-07-07T20:10:01Z`)
- Calculates MTTR as the time delta between those two values
- Converts total time to hours for reporting
- Saves the results to an `.xlsx` file

---

## 📁 Input Format

The script is designed to work with:
- `.html` or `.mhtml` files
- Exported via **Save as Webpage, Complete** from Arctic Wolf or similar dashboards

---

## 📦 Requirements

Install dependencies using pip:

```
pip install beautifulsoup4 pandas python-dateutil
```

---

## 🧪 How to Run

Open your terminal or command prompt and run:

```
python mttr_report_generator.py
```

This will launch an interactive prompt to:
1. Enter the folder path containing your `.html` or `.mhtml` ticket files
2. Enter the desired filename for the Excel report

---

## 📊 Example Output

The resulting Excel sheet includes:

| ticket_id | created_at         | occurred_at        | mttr             | mttr_hours |
|-----------|--------------------|--------------------|------------------|-------------|
| 10500000  | Jul 7, 2025 4:36PM | 2025-07-07T20:10Z  | 1:34:00          | 1.57        |

---

## 🔒 Security

- This script runs locally and does **not** upload data or connect to the internet.
- No sensitive Arctic Wolf information is included in this tool or repository.
- Always ensure you redact any sensitive files before testing or sharing.

---

## 🧠 Author Notes

This project was built out of necessity to reduce time spent manually reviewing incident tickets and calculating MTTR across large batches. It’s a small but powerful tool that brings speed and structure to SOC workflows.

If you’re working in incident response or audit reporting, this might save you hours each week. ✨

---

## 📜 License

MIT License — feel free to modify and reuse with proper credit.
