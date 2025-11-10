import json
import logging

def export_to_json(data, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Exported {len(data)} jobs to JSON: {filepath}")
    except Exception as e:
        logging.error(f"Error exporting JSON: {e}")