import cv2
import numpy as np


def draw_adaptive_beam(
    frame,
    intensity,
    direction
):

    height, width = frame.shape[:2]

    overlay = frame.copy()

    # ------------------------------------------------
    # Headlight origin
    # ------------------------------------------------

    origin_x = width // 2
    origin_y = height - 60

    # ------------------------------------------------
    # Beam direction
    # ------------------------------------------------

    if direction == "DOWNWARD":

        left_point = (
            int(width * 0.40),
            height
        )

        right_point = (
            int(width * 0.60),
            height
        )

    elif direction == "SLIGHTLY DOWNWARD":

        left_point = (
            int(width * 0.28),
            int(height * 0.78)
        )

        right_point = (
            int(width * 0.72),
            int(height * 0.78)
        )

    else:

        left_point = (
            int(width * 0.08),
            int(height * 0.55)
        )

        right_point = (
            int(width * 0.92),
            int(height * 0.55)
        )

    # ------------------------------------------------
    # Beam polygon
    # ------------------------------------------------

    polygon = np.array([
        [
            origin_x - 35,
            origin_y
        ],

        left_point,

        right_point,

        [
            origin_x + 35,
            origin_y
        ]
    ], dtype=np.int32)

    # ------------------------------------------------
    # Draw beam
    # ------------------------------------------------

    cv2.fillPoly(
        overlay,
        [polygon],
        (180, 180, 120)
    )

    # ------------------------------------------------
    # Beam transparency
    # ------------------------------------------------

    alpha = (
        intensity / 100.0
    ) * 0.18

    alpha = max(
        0.03,
        min(alpha, 0.18)
    )

    frame = cv2.addWeighted(
        overlay,
        alpha,
        frame,
        1 - alpha,
        0
    )

    # ------------------------------------------------
    # Headlight source
    # ------------------------------------------------

    cv2.circle(
        frame,
        (
            origin_x,
            origin_y
        ),
        10,
        (255, 255, 255),
        -1
    )

    return frame


def draw_inside_status(
    frame,
    glare_score,
    glare_level,
    beam_intensity,
    beam_direction
):

    height, width = frame.shape[:2]

    # ------------------------------------------------
    # Large status box
    # ------------------------------------------------

    panel_width = min(
        390,
        max(300, width // 2)
    )

    panel_height = 220

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (15, 15),
        (
            panel_width,
            panel_height
        ),
        (15, 15, 15),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.78,
        frame,
        0.22,
        0
    )

    # ------------------------------------------------
    # Glare color
    # ------------------------------------------------

    if glare_level == "HIGH":

        glare_color = (
            0,
            0,
            255
        )

        glare_text = "HIGH GLARE"

    elif glare_level == "MEDIUM":

        glare_color = (
            0,
            165,
            255
        )

        glare_text = "MEDIUM GLARE"

    else:

        glare_color = (
            0,
            255,
            0
        )

        glare_text = "LOW GLARE"

    # ------------------------------------------------
    # Title
    # ------------------------------------------------

    cv2.putText(
        frame,
        "ANTI-GLARE STATUS",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    # ------------------------------------------------
    # Glare level
    # ------------------------------------------------

    cv2.putText(
        frame,
        glare_text,
        (30, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.95,
        glare_color,
        3
    )

    # ------------------------------------------------
    # Score
    # ------------------------------------------------

    cv2.putText(
        frame,
        f"SCORE: {glare_score}/100",
        (30, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # ------------------------------------------------
    # Beam
    # ------------------------------------------------

    cv2.putText(
        frame,
        f"BEAM: {beam_intensity}%",
        (30, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (255, 255, 255),
        2
    )

    # ------------------------------------------------
    # Direction
    # ------------------------------------------------

    cv2.putText(
        frame,
        beam_direction,
        (30, 205),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (255, 255, 255),
        2
    )

    return frame