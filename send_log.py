import os, json, urllib.request, datetime

url = os.getenv("LOGSTASH_URL")
if not url:
    print("No LOGSTASH_URL set, skipping")
    exit(0)

payload = {
    "timestamp":   datetime.datetime.utcnow().isoformat() + "Z",
    "level":       "INFO" if os.getenv("JOB_STATUS") == "success" else "ERROR",
    "message":     "CI run " + os.getenv("JOB_STATUS", "unknown"),
    "app":         os.getenv("APP_NAME", "my-python-app"),
    "environment": "ci",
    "conclusion":  os.getenv("JOB_STATUS", "unknown"),
    "run_number":  int(os.getenv("GITHUB_RUN_NUMBER", 0)),
    "branch":      os.getenv("GITHUB_REF_NAME", ""),
    "actor":       os.getenv("GITHUB_ACTOR", ""),
    "repository":  os.getenv("GITHUB_REPOSITORY", ""),
}

data = json.dumps(payload).encode()
req  = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
urllib.request.urlopen(req, timeout=5)
print("Log sent to ELK ✓")
