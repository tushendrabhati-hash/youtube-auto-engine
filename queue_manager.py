import subprocess
import json
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

VIDEO_FILE = "videos.txt"
STATE_FILE = "state.json"

MAX_PARALLEL_DOWNLOADS = 3


# -----------------------
# CREATE JOB FOLDER
# -----------------------
def create_job_folder(index, vid):

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    job_id = f"{index:03d}_{vid}"

    folder = os.path.join("jobs", f"{ts}_{job_id}")
    os.makedirs(folder, exist_ok=True)

    return folder, job_id


# -----------------------
# ANALYTICS
# -----------------------
def run_analytics():
    from analytics_scheduler import run_pending_checks
    run_pending_checks()


# -----------------------
# DETECT
# -----------------------
def run_detect():

    print("\n🔎 Running Detect Step...\n")

    if os.path.exists("detect.py"):
        subprocess.run(["python", "detect.py"], check=True)


# -----------------------
# STATE
# -----------------------
def load_state():

    if not os.path.exists(STATE_FILE):
        return {"processed": []}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)

    state.setdefault("processed", [])
    return state


def save_state(state):

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# -----------------------
# GET URLS
# -----------------------
def get_urls():

    urls = []

    if not os.path.exists(VIDEO_FILE):
        return urls

    with open(VIDEO_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("NEW_VIDEO::"):
                vid = line.split("::")[1]
                urls.append((f"https://www.youtube.com/watch?v={vid}", vid))

    return urls


# -----------------------
# DOWNLOAD INTO JOB
# -----------------------
def download_one(args):

    url, vid, job_folder = args

    print(f"⬇ Downloading → {vid}")

    result = subprocess.run(
        ["python", "download.py", url, job_folder],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        return None

    return vid


# -----------------------
# PROCESS PIPELINE
# -----------------------
def process_pipeline(vid, job_folder):

    print(f"\n🎬 Processing → {vid}")

    from auto_recovery import safe_run

    safe_run(
        "hook_detect",
        subprocess.run,
        ["python", "hook_detector.py", job_folder],
        check=True
    )

    safe_run(
        "edit_step",
        subprocess.run,
        ["python", "edit.py", job_folder],
        check=True
    )

    safe_run(
        "metadata_step",
        subprocess.run,
        ["python", "metadata.py", job_folder],
        check=True
    )

    safe_run(
        "thumbnail_step",
        subprocess.run,
        ["python", "thumbnail_ai.py", job_folder],
        check=True
    )

    # IMPORTANT: upload should NOT be retried internally
    subprocess.run(
        ["python", "Upload.py", job_folder],
        check=True
    )


# -----------------------
# MAIN
# -----------------------
def run_queue():

    run_analytics()
    run_detect()

    from humanizer import session_break
    session_break()

    state = load_state()

    processed = set(state["processed"])
    urls = get_urls()

    pending = [x for x in urls if x[1] not in processed]

    print(f"\n🎯 Pending videos: {len(pending)}\n")

    if not pending:
        print("⚠ No new videos")
        return

    # ----- CREATE JOBS FIRST -----
    jobs = []
    for i, (url, vid) in enumerate(pending, start=1):
        job_folder, job_id = create_job_folder(i, vid)
        jobs.append((url, vid, job_folder))

    # ----- DOWNLOAD PARALLEL -----
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_DOWNLOADS) as ex:
        results = list(ex.map(download_one, jobs))

    successful = [j for j, r in zip(jobs, results) if r]

    print("\n✅ Downloads Finished\n")

    # ----- PROCESS SEQUENTIAL -----
    for url, vid, job_folder in successful:

        process_pipeline(vid, job_folder)

        state = load_state()
        state["processed"].append(vid)
        save_state(state)

    print("\n✅ FULL PIPELINE COMPLETE\n")


# -----------------------
if __name__ == "__main__":
    run_queue()