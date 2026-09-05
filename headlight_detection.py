import cv2
import numpy as np


def detect_headlights(
    frame,
    vehicle_bbox
):

    x1, y1, x2, y2 = vehicle_bbox

    frame_height, frame_width = (
        frame.shape[:2]
    )

    x1 = max(
        0,
        x1
    )

    y1 = max(
        0,
        y1
    )

    x2 = min(
        frame_width,
        x2
    )

    y2 = min(
        frame_height,
        y2
    )

    vehicle_roi = frame[
        y1:y2,
        x1:x2
    ]

    if vehicle_roi.size == 0:

        return []

    gray = cv2.cvtColor(
        vehicle_roi,
        cv2.COLOR_BGR2GRAY
    )

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # ========================================================
    # BRIGHT PIXEL DETECTION
    # ========================================================

    threshold_value = 220

    _, bright_mask = cv2.threshold(
        blurred,
        threshold_value,
        255,
        cv2.THRESH_BINARY
    )

    kernel = np.ones(
        (3, 3),
        np.uint8
    )

    bright_mask = cv2.morphologyEx(
        bright_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    bright_mask = cv2.morphologyEx(
        bright_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        bright_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    headlights = []

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area < 3:

            continue

        hx, hy, hw, hh = (
            cv2.boundingRect(
                contour
            )
        )

        region = gray[
            hy:hy + hh,
            hx:hx + hw
        ]

        if region.size == 0:

            continue

        brightness = float(
            np.mean(region)
        )

        max_brightness = int(
            np.max(region)
        )

        headlights.append(
            {
                "bbox": (
                    x1 + hx,
                    y1 + hy,
                    x1 + hx + hw,
                    y1 + hy + hh
                ),
                "brightness": brightness,
                "max_brightness": max_brightness,
                "area": area
            }
        )

    return headlights