import logging
import requests

logger = logging.getLogger(__name__)

def fetch_jobs(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    logger.info("Fetching jobs for %s", slug)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    jobs = response.json()["jobs"]
    logger.info("Got %d jobs for %s", len(jobs), slug)
    return jobs

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    jobs = fetch_jobs("cloudbeds")
    print(jobs[0]['title'])