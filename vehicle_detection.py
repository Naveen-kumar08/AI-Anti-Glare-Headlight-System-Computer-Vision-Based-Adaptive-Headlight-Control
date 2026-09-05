from ultralytics import YOLO


# ============================================================
# YOLO MODEL
# ============================================================

model = YOLO("yolo11n.pt")


# ============================================================
# VEHICLE CLASSES
# ============================================================

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}


# ============================================================
# VEHICLE DETECTION
# ============================================================

def detect_vehicles(
    frame,
    confidence=0.35
):

    results = model(
        frame,
        conf=confidence,
        verbose=False
    )

    detections = []

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(
                box.cls[0]
            )

            conf = float(
                box.conf[0]
            )

            if class_id not in VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            center_x = int(
                (x1 + x2) / 2
            )

            center_y = int(
                (y1 + y2) / 2
            )

            vehicle_width = x2 - x1
            vehicle_height = y2 - y1

            detections.append(
                {
                    "class_id": class_id,
                    "class_name": VEHICLE_CLASSES[class_id],
                    "confidence": conf,
                    "bbox": (
                        x1,
                        y1,
                        x2,
                        y2
                    ),
                    "center": (
                        center_x,
                        center_y
                    ),
                    "width": vehicle_width,
                    "height": vehicle_height
                }
            )

    return detections