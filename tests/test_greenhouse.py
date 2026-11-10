import json 
from src.extract.greenhouse import parse_job

def load_sample():
    with open("data/samples/greenhouse_cloudbeds.json") as f:
        return json.load(f)["jobs"]

def test_parse_job_returns_standard_keys():
    job = parse_job(load_sample()[0])
    assert set(job.keys()) == {"job_id", "title", "location", "url", "published_at"}

def test_parse_job_reads_nested_location():
    job = parse_job(load_sample()[0])
    assert isinstance(job["location"], str)
    assert job["url"].startswith("https://")