import cv2
import os
import csv
import subprocess
import tempfile
import numpy as np
import imageio_ffmpeg

from vehicle_detection import detect_vehicles
from vehicle_tracker import VehicleTracker
from headlight_detection import detect_headlights
from glare_analysis import calculate_glare_score
from beam_control import determine_beam_action


# ============================================================
# TEXT
# ============================================================

def put_text(
    image,
    text,
    position,
    font_scale,
    thickness,
    color=(0, 0, 0)
):

    cv2.putText(
        image,
        str(text),
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA
    )


# ============================================================
# CENTER TEXT
# ============================================================

def centered_text(
    image,
    text,
    y,
    font_scale,
    thickness,
    color=(0, 0, 0)
):

    font = cv2.FONT_HERSHEY_SIMPLEX

    text_size = cv2.getTextSize(
        str(text),
        font,
        font_scale,
        thickness
    )[0]

    x = int(
        (image.shape[1] - text_size[0]) / 2
    )

    x = max(
        10,
        x
    )

    cv2.putText(
        image,
        str(text),
        (x, y),
        font,
        font_scale,
        color,
        thickness,
        cv2.LINE_AA
    )


# ============================================================
# GLARE COLOR
# ============================================================

def glare_color(level):

    if level == "HIGH":

        return (
            0,
            0,
            220
        )

    if level == "MEDIUM":

        return (
            0,
            120,
            220
        )

    return (
        0,
        140,
        0
    )


# ============================================================
# HORIZONTAL LINE
# ============================================================

def draw_line(
    image,
    y,
    thickness=2
):

    cv2.line(
        image,
        (20, y),
        (
            image.shape[1] - 20,
            y
        ),
        (0, 0, 0),
        thickness
    )


# ============================================================
# H264 CONVERSION
# ============================================================

def convert_to_h264(
    input_file,
    output_file
):

    ffmpeg = (
        imageio_ffmpeg.get_ffmpeg_exe()
    )

    command = [
        ffmpeg,

        "-y",

        "-i",
        input_file,

        "-c:v",
        "libx264",

        "-preset",
        "veryfast",

        "-crf",
        "23",

        "-pix_fmt",
        "yuv420p",

        "-movflags",
        "+faststart",

        output_file
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            "H.264 conversion failed:\n"
            + result.stderr[-3000:]
        )

    if not os.path.exists(
        output_file
    ):

        raise RuntimeError(
            "H.264 output was not created."
        )


# ============================================================
# PROCESS VIDEO
# ============================================================

def process_video(
    input_path,
    output_path
):

    cap = cv2.VideoCapture(
        input_path
    )

    if not cap.isOpened():

        raise ValueError(
            "Could not open input video."
        )


    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    width = int(
        cap.get(
            cv2.CAP_PROP_FRAME_WIDTH
        )
    )

    height = int(
        cap.get(
            cv2.CAP_PROP_FRAME_HEIGHT
        )
    )

    total_frames = int(
        cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )
    )


    if fps <= 0:

        fps = 30


    if width <= 0 or height <= 0:

        cap.release()

        raise ValueError(
            "Invalid video dimensions."
        )


    # ========================================================
    # PANEL
    # ========================================================

    panel_width = max(
        650,
        int(width * 0.42)
    )

    output_width = (
        width +
        panel_width
    )


    # ========================================================
    # DIRECTORIES
    # ========================================================

    output_dir = os.path.dirname(
        output_path
    )

    if output_dir:

        os.makedirs(
            output_dir,
            exist_ok=True
        )

    os.makedirs(
        "results",
        exist_ok=True
    )


    # ========================================================
    # TEMP FILE
    # ========================================================

    temp_directory = tempfile.mkdtemp()

    temp_avi = os.path.join(
        temp_directory,
        "processed.avi"
    )


    # ========================================================
    # VIDEO WRITER
    # ========================================================

    fourcc = cv2.VideoWriter_fourcc(
        *"XVID"
    )

    out = cv2.VideoWriter(
        temp_avi,
        fourcc,
        fps,
        (
            output_width,
            height
        )
    )

    if not out.isOpened():

        cap.release()

        raise RuntimeError(
            "Could not create temporary video."
        )


    # ========================================================
    # CSV
    # ========================================================

    output_name = os.path.splitext(
        os.path.basename(
            output_path
        )
    )[0]

    csv_path = os.path.join(
        "results",
        output_name + "_report.csv"
    )


    csv_file = open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8"
    )

    csv_writer = csv.writer(
        csv_file
    )


    csv_writer.writerow(
        [
            "Frame",
            "Vehicles",
            "Approaching Vehicles",
            "Headlights",
            "Glare Score",
            "Glare Level",
            "Beam Intensity",
            "Beam Direction",
            "Action"
        ]
    )


    # ========================================================
    # TRACKER
    # ========================================================

    tracker = VehicleTracker()


    # ========================================================
    # COUNTERS
    # ========================================================

    frame_number = 0

    high_glare_frames = 0

    medium_glare_frames = 0

    low_glare_frames = 0


    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:

            break


        frame_number += 1


        # ====================================================
        # VEHICLES
        # ====================================================

        detections = detect_vehicles(
            frame
        )

        detections = tracker.update(
            detections
        )


        approaching_count = 0

        total_headlights = 0

        highest_glare_score = 0

        highest_glare_level = "LOW"

        current_beam_action = (
            determine_beam_action(
                "LOW"
            )
        )


        # ====================================================
        # EACH VEHICLE
        # ====================================================

        for detection in detections:

            x1, y1, x2, y2 = (
                detection["bbox"]
            )

            class_name = (
                detection["class_name"]
            )

            confidence = (
                detection["confidence"]
            )

            direction = (
                detection["direction"]
            )


            # ------------------------------------------------
            # HEADLIGHT
            # ------------------------------------------------

            headlights = (
                detect_headlights(
                    frame,
                    detection["bbox"]
                )
            )

            total_headlights += (
                len(headlights)
            )


            approaching = (
                direction ==
                "APPROACHING"
            )


            if approaching:

                approaching_count += 1


            # ------------------------------------------------
            # GLARE
            # ------------------------------------------------

            glare = (
                calculate_glare_score(
                    headlights,
                    approaching
                )
            )


            glare_score = glare[
                "score"
            ]

            glare_level = glare[
                "level"
            ]


            if (
                glare_score
                >
                highest_glare_score
            ):

                highest_glare_score = (
                    glare_score
                )

                highest_glare_level = (
                    glare_level
                )

                current_beam_action = (
                    determine_beam_action(
                        glare_level
                    )
                )


            # ------------------------------------------------
            # GLARE COUNTERS
            # ------------------------------------------------

            if glare_level == "HIGH":

                high_glare_frames += 1

            elif glare_level == "MEDIUM":

                medium_glare_frames += 1

            else:

                low_glare_frames += 1


            # =================================================
            # VEHICLE BOX
            # =================================================

            if approaching:

                box_color = (
                    0,
                    0,
                    255
                )

                label = (
                    "OPPOSING "
                    +
                    class_name.upper()
                    +
                    " "
                    +
                    f"{confidence:.2f}"
                )

            else:

                box_color = (
                    0,
                    180,
                    0
                )

                label = (
                    class_name.upper()
                    +
                    " "
                    +
                    f"{confidence:.2f}"
                )


            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                box_color,
                5
            )


            put_text(
                frame,
                label,
                (
                    x1,
                    max(
                        45,
                        y1 - 15
                    )
                ),
                0.9,
                3,
                box_color
            )


            # =================================================
            # HEADLIGHT BOX
            # =================================================

            for light in headlights:

                hx1, hy1, hx2, hy2 = (
                    light["bbox"]
                )


                cv2.rectangle(
                    frame,
                    (hx1, hy1),
                    (hx2, hy2),
                    (255, 0, 0),
                    5
                )


                cx = int(
                    (hx1 + hx2) / 2
                )

                cy = int(
                    (hy1 + hy2) / 2
                )


                cv2.circle(
                    frame,
                    (cx, cy),
                    15,
                    (255, 0, 0),
                    -1
                )


                put_text(
                    frame,
                    "HEADLIGHT",
                    (
                        hx1,
                        max(
                            35,
                            hy1 - 10
                        )
                    ),
                    0.7,
                    3,
                    (255, 0, 0)
                )


        # ====================================================
        # BEAM INFORMATION
        # ====================================================

        beam_intensity = (
            current_beam_action[
                "beam_intensity"
            ]
        )

        beam_direction = (
            current_beam_action[
                "beam_angle"
            ]
        )

        action = (
            current_beam_action[
                "action"
            ]
        )


        # ====================================================
        # WHITE PANEL
        # ====================================================

        panel = np.full(
            (
                height,
                panel_width,
                3
            ),
            255,
            dtype=np.uint8
        )


        cv2.rectangle(
            panel,
            (2, 2),
            (
                panel_width - 3,
                height - 3
            ),
            (0, 0, 0),
            4
        )


        # ====================================================
        # RESPONSIVE SCALE
        # ====================================================

        scale = max(
            0.75,
            min(
                1.35,
                height / 900
            )
        )


        # ====================================================
        # HEADER
        # ====================================================

        centered_text(
            panel,
            "AI ANTI-GLARE",
            int(55 * scale),
            0.95 * scale,
            4
        )

        centered_text(
            panel,
            "HEADLIGHT SYSTEM",
            int(100 * scale),
            0.72 * scale,
            3
        )


        draw_line(
            panel,
            int(120 * scale),
            3
        )


        # ====================================================
        # LARGE GLARE LEVEL
        # ====================================================

        glare_text_color = glare_color(
            highest_glare_level
        )


        put_text(
            panel,
            "GLARE LEVEL",
            (
                30,
                int(160 * scale)
            ),
            0.7 * scale,
            3,
            (70, 70, 70)
        )


        put_text(
            panel,
            highest_glare_level,
            (
                30,
                int(225 * scale)
            ),
            1.35 * scale,
            5,
            glare_text_color
        )


        # ====================================================
        # LARGE GLARE SCORE
        # ====================================================

        put_text(
            panel,
            "GLARE SCORE",
            (
                30,
                int(275 * scale)
            ),
            0.7 * scale,
            3,
            (70, 70, 70)
        )


        put_text(
            panel,
            f"{highest_glare_score} / 100",
            (
                30,
                int(335 * scale)
            ),
            1.1 * scale,
            5,
            (0, 0, 0)
        )


        draw_line(
            panel,
            int(360 * scale),
            2
        )


        # ====================================================
        # INFORMATION AREA
        # ====================================================

        info_y = int(
            405 * scale
        )

        line_gap = int(
            58 * scale
        )


        # VEHICLES

        put_text(
            panel,
            f"VEHICLES: {len(detections)}",
            (
                30,
                info_y
            ),
            0.65 * scale,
            3,
            (0, 0, 0)
        )


        info_y += line_gap


        # APPROACHING

        put_text(
            panel,
            f"APPROACHING: {approaching_count}",
            (
                30,
                info_y
            ),
            0.65 * scale,
            3,
            (0, 0, 180)
        )


        info_y += line_gap


        # HEADLIGHTS

        put_text(
            panel,
            f"HEADLIGHTS: {total_headlights}",
            (
                30,
                info_y
            ),
            0.65 * scale,
            3,
            (120, 70, 0)
        )


        info_y += line_gap


        # BEAM INTENSITY

        put_text(
            panel,
            f"BEAM INTENSITY: {beam_intensity}%",
            (
                30,
                info_y
            ),
            0.65 * scale,
            3,
            (0, 0, 0)
        )


        info_y += line_gap


        # BEAM DIRECTION

        direction_display = (
            "SLIGHT DOWN"
            if beam_direction ==
            "SLIGHTLY DOWNWARD"
            else beam_direction
        )


        put_text(
            panel,
            f"BEAM: {direction_display}",
            (
                30,
                info_y
            ),
            0.62 * scale,
            3,
            (0, 0, 0)
        )


        # ====================================================
        # SYSTEM ACTION
        # ====================================================

        action_y = (
            height -
            int(65 * scale)
        )


        if highest_glare_level == "HIGH":

            action_display = (
                "DIM + REDIRECT"
            )

        elif highest_glare_level == "MEDIUM":

            action_display = (
                "REDUCE BEAM"
            )

        else:

            action_display = (
                "NORMAL BEAM"
            )


        put_text(
            panel,
            f"ACTION: {action_display}",
            (
                30,
                action_y
            ),
            0.65 * scale,
            4,
            glare_text_color
        )


        # ====================================================
        # COMBINE
        # ====================================================

        combined_frame = np.hstack(
            [
                frame,
                panel
            ]
        )


        # ====================================================
        # CSV
        # ====================================================

        csv_writer.writerow(
            [
                frame_number,
                len(detections),
                approaching_count,
                total_headlights,
                highest_glare_score,
                highest_glare_level,
                beam_intensity,
                beam_direction,
                action
            ]
        )


        # ====================================================
        # WRITE
        # ====================================================

        out.write(
            combined_frame
        )


    # ========================================================
    # CLOSE
    # ========================================================

    cap.release()

    out.release()

    csv_file.close()


    # ========================================================
    # CONVERT
    # ========================================================

    convert_to_h264(
        temp_avi,
        output_path
    )


    # ========================================================
    # CLEAN TEMP
    # ========================================================

    try:

        os.remove(
            temp_avi
        )

        os.rmdir(
            temp_directory
        )

    except Exception:

        pass


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "fps":
            fps,

        "width":
            width,

        "height":
            height,

        "output_width":
            output_width,

        "panel_width":
            panel_width,

        "total_frames":
            total_frames,

        "high_glare_frames":
            high_glare_frames,

        "medium_glare_frames":
            medium_glare_frames,

        "low_glare_frames":
            low_glare_frames,

        "csv_path":
            csv_path
    }