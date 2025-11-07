from datetime import datetime
import os

LOG_DIR = "validation/performance_logs"
LOG_FILE = os.path.join(LOG_DIR, "runs.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log(message: str):
    timestamp = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"logged: {message}")

if __name__ == "__main__":
    log("manual run – testing logging pipeline")
