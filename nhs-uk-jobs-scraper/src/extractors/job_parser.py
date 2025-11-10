from bs4 import BeautifulSoup

def parse_job_card(card):
    try:
        title = card.select_one(".nhsuk-card__heading a").get_text(strip=True)
        link = card.select_one(".nhsuk-card__heading a")["href"]
        location = card.select_one(".nhsuk-card__location").get_text(strip=True) if card.select_one(".nhsuk-card__location") else "N/A"
        salary = card.select_one(".nhsuk-card__salary").get_text(strip=True) if card.select_one(".nhsuk-card__salary") else "N/A"
        posting_date = card.select_one(".nhsuk-card__date--posted").get_text(strip=True) if card.select_one(".nhsuk-card__date--posted") else "N/A"
        closing_date = card.select_one(".nhsuk-card__date--closing").get_text(strip=True) if card.select_one(".nhsuk-card__date--closing") else "N/A"

        return {
            "jobTitle": title,
            "salary": salary,
            "location": location,
            "qualifications": "See listing for details",
            "postingDate": posting_date,
            "closingDate": closing_date,
            "contactDetails": "See NHS listing",
            "documents": [link],
            "apify_monitoring_status": "new"
        }
    except Exception:
        return None