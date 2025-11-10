import json
import logging
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from src.extractors.job_parser import parse_job_card
from src.outputs.json_exporter import export_to_json
from src.outputs.csv_exporter import export_to_csv
from src.extractors.utils import load_settings, delta_filter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_jobs(start_url: str, max_pages: int = 5, output_format: str = "json"):
    logging.info("Starting NHS UK job scraping process...")
    settings = load_settings()

    all_jobs = []
    session = requests.Session()

    for page in range(1, max_pages + 1):
        url = f"{start_url}&page={page}"
        logging.info(f"Fetching page {page}: {url}")
        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.select(".nhsuk-card")  # adjust based on site structure
        if not job_cards:
            logging.warning("No job cards found, stopping early.")
            break

        for job_card in job_cards:
            job_data = parse_job_card(job_card)
            if job_data:
                all_jobs.append(job_data)

        time.sleep(settings.get("requestDelay", 2))

    logging.info(f"Scraped {len(all_jobs)} total job listings before delta filtering.")
    all_jobs = delta_filter(all_jobs, settings.get("previousDataPath", "data/sample_output.json"))

    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)

    if output_format == "json":
        export_to_json(all_jobs, output_dir / "latest_output.json")
    elif output_format == "csv":
        export_to_csv(all_jobs, output_dir / "latest_output.csv")
    else:
        logging.warning(f"Unsupported format: {output_format}. Defaulting to JSON.")
        export_to_json(all_jobs, output_dir / "latest_output.json")

    logging.info("Scraping completed successfully.")

if __name__ == "__main__":
    cfg = load_settings()
    scrape_jobs(cfg["startUrl"], cfg.get("maxPagesToScrape", 5), cfg.get("outputFormat", "json"))