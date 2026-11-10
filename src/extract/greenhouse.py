import requests

def fetch_jobs(slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data["jobs"]

if __name__ == "__main__":
    jobs = fetch_jobs("cloudbeds")
    print(f"Found {len(jobs)} jobs")
    print(jobs[0]['title'])