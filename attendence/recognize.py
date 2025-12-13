import cv2
import face_recognition
import pickle
import os

# Path to saved encodings
ENCODING_FILE = "../encodings.pkl"

# Load known encodings
if not os.path.exists(ENCODING_FILE):
    print("No encodings found! Run enrollment first.")
    exit()

with open(ENCODING_FILE, "rb") as f:
    data = pickle.load(f)
    known_ids = data.get("ids", [])
    known_encodings = data.get("encodings", [])

# Start webcam
cap = cv2.VideoCapture(0)
print("Press 'q' to quit recognition")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_ids = []

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)

        if len(face_distances) > 0:
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                face_ids.append(known_ids[best_match_index])
            else:
                face_ids.append("Unknown")
        else:
            face_ids.append("Unknown")

    # Draw rectangles and IDs
    for (top, right, bottom, left), face_id in zip(face_locations, face_ids):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, face_id, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        print(f"Detected: {face_id}")

    cv2.imshow("Recognition", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()