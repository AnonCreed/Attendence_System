import cv2
import face_recognition
import pickle
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

ENCODING_FILE = "../encodings.pkl"
FACE_MATCH_THRESHOLD = 0.6  # lower = stricter

# ---------------- LOAD DATABASE ----------------
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "rb") as f:
        data = pickle.load(f)
        known_ids = data.get("ids", [])
        known_encodings = data.get("encodings", [])
else:
    known_ids = []
    known_encodings = []

# ---------------- GET STUDENT ID ----------------
student_id = input("Enter student ID: ").strip()

if student_id in known_ids:
    print(f"[ERROR] ID {student_id} already exists. Enrollment blocked.")
    exit()

# ---------------- CHOOSE MODE ----------------
mode = input("Enroll via webcam or file? (webcam/file): ").strip().lower()

# ---------------- CAPTURE IMAGE ----------------
if mode == "webcam":
    cap = cv2.VideoCapture(0)
    print("Press 'q' to capture face")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        cv2.imshow("Enrollment", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            capture_frame = frame
            break

    cap.release()
    cv2.destroyAllWindows()

elif mode == "file":
    Tk().withdraw()
    file_path = askopenfilename(
        title="Select face image",
        filetypes=[("Image files", "*.jpg *.png *.jpeg")]
    )
    if not file_path:
        print("[ERROR] No image selected.")
        exit()

    capture_frame = cv2.imread(file_path)
    if capture_frame is None:
        print("[ERROR] Failed to load image.")
        exit()

else:
    print("[ERROR] Invalid mode selected.")
    exit()

# ---------------- FACE PROCESSING ----------------
rgb_frame = cv2.cvtColor(capture_frame, cv2.COLOR_BGR2RGB)
face_locations = face_recognition.face_locations(rgb_frame)

if len(face_locations) != 1:
    print(f"[ERROR] Expected exactly 1 face, found {len(face_locations)}.")
    exit()

encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

# ---------------- DUPLICATE FACE CHECK ----------------
if known_encodings:
    distances = face_recognition.face_distance(known_encodings, encoding)
    best_match_index = distances.argmin()

    if distances[best_match_index] < FACE_MATCH_THRESHOLD:
        print(
            f"[BLOCKED] Face already enrolled as ID "
            f"{known_ids[best_match_index]}"
        )
        exit()

# ---------------- SAVE ----------------
known_ids.append(student_id)
known_encodings.append(encoding)

with open(ENCODING_FILE, "wb") as f:
    pickle.dump(
        {"ids": known_ids, "encodings": known_encodings},
        f
    )

print(f"[SUCCESS] Student {student_id} enrolled successfully!")
