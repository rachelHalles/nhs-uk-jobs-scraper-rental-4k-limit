import json
import logging
from pathlib import Path

def load_settings():
    config_path = Path("src/config/settings.json")
    with open(config_path, "r") as f:
        return json.load(f)

def delta_filter(jobs, previous_path):
    prev_data = []
    previous = Path(previous_path)
    if previous.exists():
        with open(previous, "r") as f:
            prev_data = json.load(f)

    prev_titles = {job["jobTitle"] for job in prev_data}
    new_jobs = [j for j in jobs if j["jobTitle"] not in prev_titles]

    for job in prev_data:
        if job["jobTitle"] not in [j["jobTitle"] for j in jobs]:
            job["apify_monitoring_status"] = "delisted"
            new_jobs.append(job)

    logging.info(f"Delta filter result: {len(new_jobs)} new/delisted jobs identified.")
    return new_jobs