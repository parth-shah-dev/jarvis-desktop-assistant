import cv2
import os
import numpy as np

# ==== CONFIG ====
MODEL_NAME = "trained_model.yml"   # File that will be created
CASCADE_PATH = "haarcascade_frontalface_default.xml"  # Must be in same folder
PERSON_ID = 1                      # ID for your face (you can use 1 for yourself)
NUM_SAMPLES = 40                   # Number of face images to capture

# ==== CHECK CASCADE ====
if not os.path.exists(CASCADE_PATH):
    print(f"[ERROR] Haarcascade file not found: {CASCADE_PATH}")
    print("Download 'haarcascade_frontalface_default.xml' and place it in this folder.")
    exit(1)

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
if face_cascade.empty():
    print("[ERROR] Failed to load Haarcascade. Check the file path.")
    exit(1)

# ==== START CAMERA ====
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Cannot open camera")
    exit(1)

print("[INFO] Camera opened. Look at the camera...")
print("[INFO] Press 'q' to stop early if needed.")

faces = []
labels = []
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to grab frame from camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    detected_faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in detected_faces:
        # Draw rectangle just for visualization
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

        # Extract face region of interest (ROI)
        face_roi = gray[y:y + h, x:x + w]

        # Normalize size (optional but helps consistency)
        face_roi = cv2.resize(face_roi, (200, 200))

        faces.append(face_roi)
        labels.append(PERSON_ID)
        count += 1

        cv2.putText(
            frame,
            f"Samples: {count}/{NUM_SAMPLES}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        print(f"[INFO] Captured sample {count}/{NUM_SAMPLES}")

        # Stop when enough samples collected
        if count >= NUM_SAMPLES:
            break

    cv2.imshow("Capturing Your Face - Press 'q' to quit", frame)

    # Exit early if user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Stopped by user.")
        break

    if count >= NUM_SAMPLES:
        print("[INFO] Collected all samples.")
        break

# Cleanup camera
cap.release()
cv2.destroyAllWindows()

if len(faces) == 0:
    print("[ERROR] No faces captured. Try again with better lighting and face visible.")
    exit(1)

# ==== TRAIN LBPH MODEL ====
print("[INFO] Training LBPH face recognizer...")

recognizer = cv2.face.LBPHFaceRecognizer_create()
faces_np = np.array(faces)
labels_np = np.array(labels)

recognizer.train(faces_np, labels_np)
recognizer.write(MODEL_NAME)

print(f"[SUCCESS] Training complete. Model saved as: {MODEL_NAME}")
