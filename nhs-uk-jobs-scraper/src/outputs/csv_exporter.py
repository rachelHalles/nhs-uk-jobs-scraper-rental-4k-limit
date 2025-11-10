import csv
import logging

def export_to_csv(data, filepath):
    try:
        if not data:
            logging.warning("No data to export to CSV.")
            return
        keys = data[0].keys()
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Exported {len(data)} jobs to CSV: {filepath}")
    except Exception as e:
        logging.error(f"Error exporting CSV: {e}")