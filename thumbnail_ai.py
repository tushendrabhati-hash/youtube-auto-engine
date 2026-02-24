import cv2
import os
import sys
import numpy as np


# -----------------------------
# SCORE FRAME QUALITY
# -----------------------------
def calculate_score(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = gray.mean()
    contrast = gray.std()

    brightness_penalty = 0
    if brightness < 60 or brightness > 200:
        brightness_penalty = 0.5

    score = (
        sharpness * 0.6 +
        brightness * 0.2 +
        contrast * 0.2
    ) * (1 - brightness_penalty)

    return score


# -----------------------------
# CENTER CROP (SHORTS)
# -----------------------------
def crop_vertical(frame):

    h, w, _ = frame.shape

    target_ratio = 9 / 16
    new_w = int(h * target_ratio)

    if new_w < w:
        x1 = (w - new_w) // 2
        frame = frame[:, x1:x1 + new_w]

    return frame


# -----------------------------
# FIND EDITED VIDEO
# -----------------------------
def find_edit_video(job_folder):

    path = os.path.join(job_folder, "002_edit.mp4")

    if os.path.exists(path):
        return path

    print("❌ 002_edit.mp4 not found")
    return None


# -----------------------------
# PICK BEST FRAME
# -----------------------------
def pick_best_frame(job_folder):

    video_path = find_edit_video(job_folder)

    if not video_path:
        sys.exit(1)

    output_path = os.path.join(job_folder, "thumbnail.jpg")

    print("🧠 Selecting Best Thumbnail Frame...")
    print(f"📁 Source → {video_path}")

    cap = cv2.VideoCapture(video_path)

    best_score = 0
    best_frame = None
    frame_id = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # skip frames for speed
        if frame_id % 15 != 0:
            frame_id += 1
            continue

        frame = crop_vertical(frame)

        score = calculate_score(frame)

        if score > best_score:
            best_score = score
            best_frame = frame.copy()

        frame_id += 1

    cap.release()

    if best_frame is not None:

        best_frame = cv2.resize(best_frame, (1080, 1920))

        cv2.imwrite(
            output_path,
            best_frame,
            [cv2.IMWRITE_JPEG_QUALITY, 95]
        )

        print(f"✅ Thumbnail saved → {output_path}")

    else:
        print("❌ Thumbnail selection failed")
        sys.exit(1)


# -----------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ Usage: thumbnail_ai.py <job_folder>")
        sys.exit(1)

    pick_best_frame(sys.argv[1])