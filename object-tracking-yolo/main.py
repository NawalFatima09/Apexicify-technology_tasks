import cv2
import numpy as np
from ultralytics import YOLO
import time


def get_color(track_id):
    np.random.seed(int(track_id))
    color = tuple(np.random.randint(0, 255, 3).tolist())
    return (int(color[0]), int(color[1]), int(color[2]))


def main():
    # ==================== CONFIG ====================
    CONFIDENCE_THRESHOLD = 0.25
    MODEL_NAME = "yolov8n.pt"   # safer for laptop (x is too heavy)
    VIDEO_SOURCE = 0
    IMG_SIZE = 640

    print(f"Loading model: {MODEL_NAME}...")
    model = YOLO(MODEL_NAME)

    # FIX for Windows camera issue
    cap = cv2.VideoCapture(VIDEO_SOURCE, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open video source")
        return

    prev_time = time.time()
    frame_count = 0
    fps = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame")
            break

        # Resize frame
        frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

        # ==================== YOLO TRACKING ====================
        results = model.track(
            frame,
            persist=True,
            conf=CONFIDENCE_THRESHOLD,
            iou=0.3,
            tracker="bytetrack.yaml",
            imgsz=IMG_SIZE,
            verbose=False
        )

        # ==================== DRAW RESULTS ====================
        if results and results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
            class_ids = results[0].boxes.cls.cpu().numpy()
            track_ids = results[0].boxes.id

            if track_ids is not None:
                track_ids = track_ids.cpu().numpy()
            else:
                track_ids = [-1] * len(boxes)

            class_names = model.names

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)

                class_id = int(class_ids[i])
                class_name = class_names[class_id]
                conf = confidences[i]
                track_id = int(track_ids[i])

                label = f"ID:{track_id} {class_name} {conf:.2f}"
                color = get_color(track_id)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # ==================== FPS ====================
        frame_count += 1
        current_time = time.time()

        if current_time - prev_time >= 1:
            fps = frame_count
            frame_count = 0
            prev_time = current_time

        cv2.putText(frame, f"FPS: {fps}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("YOLOv8 Detection + Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()