import subprocess
import sys
import os
import time

# ==============================
# ENGINE CONFIG
# ==============================

PYTHON = sys.executable   # current python path

STEPS = [
    ("DETECT", "detect.py"),
    ("DOWNLOAD", "download.py"),
    ("EDIT", "edit.py"),
    ("UPLOAD", "Upload.py"),
]

OUTPUT_FILES = [
    "output.mp4",
    "final.mp4"
]


# ==============================
# RUN SCRIPT
# ==============================

def run_step(name, script):

    print("\n" + "=" * 35)
    print(f"🚀 Running {name}...")
    print("=" * 35)

    if not os.path.exists(script):
        print(f"❌ {script} not found")
        return False

    try:
        subprocess.run(
            [PYTHON, script],
            check=True
        )
        print(f"✅ {name} COMPLETE")
        return True

    except subprocess.CalledProcessError:
        print(f"❌ {name} FAILED")
        return False


# ==============================
# CLEANUP
# ==============================

def cleanup():

    print("\n🧹 Cleaning temp files...")

    for f in OUTPUT_FILES:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"Removed → {f}")
            except:
                pass


# ==============================
# MAIN ENGINE
# ==============================

def main():

    print("\n" + "=" * 35)
    print("🔥 YOUTUBE AUTO ENGINE START")
    print("=" * 35)

    for name, script in STEPS:

        success = run_step(name, script)

        if not success:
            print("\n🛑 PIPELINE STOPPED")
            return

        time.sleep(2)

    cleanup()

    print("\n🎉 FULL PIPELINE COMPLETE")


# ==============================

if __name__ == "__main__":
    main()