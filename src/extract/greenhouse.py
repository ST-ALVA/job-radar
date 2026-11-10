import logging
import time
import requests

logger = logging.getLogger(__name__)

MAX_RETRIES = 3

def fetch_jobs(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Fetching jobs for %s (attempt %d)", slug, attempt)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            jobs = response.json()["jobs"]
            logger.info("Got %d jobs for %s", len(jobs), slug)
            return jobs
        except requests.exceptions.RequestException as error:
            status = error.response.status_code if error.response is not None else None
            if status is not None and 400 <= status < 500 and status != 429:
                logger.error("Permanent error %d for %s, not retrying", status, slug)
                raise
            logger.warning("Attempt %d failed for %s: %s", attempt, slug, error)
            if attempt == MAX_RETRIES:
                raise
            time.sleep(2 ** attempt)

def parse_job(raw):
    return{
        "job_id": raw["id"], 
        "title": raw["title"], 
        "location": raw["location"]["name"], 
        "url": raw["absolute_url"], 
        "published_at": raw["first_published"], 
    }

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    jobs = fetch_jobs("cloudbeds")
    print(jobs[0]['title'])