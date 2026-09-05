import streamlit as st
import os
import time
import pandas as pd

from video_processor import process_video


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Anti-Glare Headlight System",
    page_icon="🚗",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "processed" not in st.session_state:

    st.session_state.processed = False


if "output_path" not in st.session_state:

    st.session_state.output_path = None


if "csv_path" not in st.session_state:

    st.session_state.csv_path = None


if "result_data" not in st.session_state:

    st.session_state.result_data = None


if "uploaded_name" not in st.session_state:

    st.session_state.uploaded_name = None


# ============================================================
# HEADER
# ============================================================

st.title(
    "AI Anti-Glare Headlight System"
)

st.subheader(
    "Computer Vision Based Adaptive Headlight Control"
)

st.write(
    "Upload a night-driving video to detect vehicles, "
    "headlights and glare conditions. The system analyzes "
    "the video and generates an adaptive beam-control result."
)

st.divider()


# ============================================================
# UPLOAD
# ============================================================

st.header(
    "1. Select Night-Driving Video"
)

uploaded_video = st.file_uploader(
    "Upload MP4 / AVI / MOV / MKV video",
    type=[
        "mp4",
        "avi",
        "mov",
        "mkv"
    ],
    accept_multiple_files=False
)


# ============================================================
# FILE INFORMATION
# ============================================================

if uploaded_video is not None:

    file_size_mb = (
        len(uploaded_video.getbuffer())
        /
        (1024 * 1024)
    )

    st.write(
        f"**File Name:** {uploaded_video.name}"
    )

    st.write(
        f"**File Size:** {file_size_mb:.2f} MB"
    )


    # ========================================================
    # SAVE INPUT
    # ========================================================

    os.makedirs(
        "input_videos",
        exist_ok=True
    )

    input_path = os.path.join(
        "input_videos",
        uploaded_video.name
    )


    with open(
        input_path,
        "wb"
    ) as file:

        file.write(
            uploaded_video.getbuffer()
        )


    # ========================================================
    # INPUT PREVIEW
    # ========================================================

    st.subheader(
        "Input Video Preview"
    )

    st.video(
        uploaded_video
    )


    # ========================================================
    # PROCESS BUTTON
    # ========================================================

    st.divider()

    process_button = st.button(
        "PROCESS VIDEO",
        type="primary",
        use_container_width=True
    )


    if process_button:

        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        st.session_state.processed = False

        st.session_state.output_path = None

        st.session_state.csv_path = None

        st.session_state.result_data = None


        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        os.makedirs(
            "output_videos",
            exist_ok=True
        )


        base_name = os.path.splitext(
            uploaded_video.name
        )[0]


        output_path = os.path.join(
            "output_videos",
            base_name +
            "_ANTI_GLARE.mp4"
        )


        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        progress = st.progress(
            0
        )

        status = st.empty()


        try:

            status.write(
                "AI system is processing the video..."
            )

            progress.progress(
                10
            )


            # ------------------------------------------------
            # PROCESS
            # ------------------------------------------------

            result = process_video(
                input_path,
                output_path
            )


            progress.progress(
                100
            )


            status.success(
                "Video processing completed successfully."
            )


            # ------------------------------------------------
            # SAVE SESSION
            # ------------------------------------------------

            st.session_state.processed = True

            st.session_state.output_path = (
                output_path
            )

            st.session_state.csv_path = (
                result["csv_path"]
            )

            st.session_state.result_data = (
                result
            )

            st.session_state.uploaded_name = (
                uploaded_video.name
            )


            time.sleep(
                0.5
            )

            st.rerun()


        except Exception as error:

            progress.empty()

            status.error(
                "Video processing failed."
            )

            st.exception(
                error
            )


# ============================================================
# RESULTS
# ============================================================

if (
    st.session_state.processed
    and
    st.session_state.output_path
    and
    os.path.exists(
        st.session_state.output_path
    )
):

    st.divider()

    st.header(
        "2. AI Anti-Glare Output"
    )


    # ========================================================
    # OUTPUT VIDEO
    # ========================================================

    st.subheader(
        "Processed Video"
    )

    st.video(
        st.session_state.output_path
    )


    # ========================================================
    # DOWNLOAD OUTPUT
    # ========================================================

    with open(
        st.session_state.output_path,
        "rb"
    ) as video_file:

        video_bytes = (
            video_file.read()
        )


    st.download_button(
        label="DOWNLOAD PROCESSED VIDEO",
        data=video_bytes,
        file_name=os.path.basename(
            st.session_state.output_path
        ),
        mime="video/mp4",
        use_container_width=True
    )


    # ========================================================
    # RESULT DATA
    # ========================================================

    result = (
        st.session_state.result_data
    )


    if result is not None:

        st.divider()

        st.header(
            "3. Processing Summary"
        )


        # ====================================================
        # METRICS
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Total Frames",
                result["total_frames"]
            )


        with col2:

            st.metric(
                "Video FPS",
                f"{result['fps']:.2f}"
            )


        with col3:

            st.metric(
                "Video Width",
                result["width"]
            )


        with col4:

            st.metric(
                "Video Height",
                result["height"]
            )


        # ====================================================
        # GLARE SUMMARY
        # ====================================================

        st.subheader(
            "Glare Frame Summary"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "HIGH Glare Frames",
                result["high_glare_frames"]
            )


        with col2:

            st.metric(
                "MEDIUM Glare Frames",
                result["medium_glare_frames"]
            )


        with col3:

            st.metric(
                "LOW Glare Frames",
                result["low_glare_frames"]
            )


    # ========================================================
    # CSV ANALYSIS
    # ========================================================

    csv_path = (
        st.session_state.csv_path
    )


    if (
        csv_path
        and
        os.path.exists(csv_path)
    ):

        st.divider()

        st.header(
            "4. CSV-Based Graphical Analysis"
        )


        # ====================================================
        # READ CSV
        # ====================================================

        df = pd.read_csv(
            csv_path
        )


        # ====================================================
        # CLEAN DATA
        # ====================================================

        numeric_columns = [
            "Frame",
            "Vehicles",
            "Approaching Vehicles",
            "Headlights",
            "Glare Score",
            "Beam Intensity"
        ]


        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )


        df = df.fillna(0)


        # ====================================================
        # GRAPH 1
        # ====================================================

        st.subheader(
            "Glare Score vs Frame"
        )


        glare_chart = df[
            [
                "Frame",
                "Glare Score"
            ]
        ].set_index(
            "Frame"
        )


        st.line_chart(
            glare_chart,
            use_container_width=True
        )


        st.caption(
            "This graph shows how the detected glare "
            "score changes throughout the video."
        )


        # ====================================================
        # GRAPH 2
        # ====================================================

        st.subheader(
            "Vehicle Detection vs Frame"
        )


        vehicle_chart = df[
            [
                "Frame",
                "Vehicles",
                "Approaching Vehicles"
            ]
        ].set_index(
            "Frame"
        )


        st.line_chart(
            vehicle_chart,
            use_container_width=True
        )


        # ====================================================
        # GRAPH 3
        # ====================================================

        st.subheader(
            "Headlights Detected vs Frame"
        )


        headlight_chart = df[
            [
                "Frame",
                "Headlights"
            ]
        ].set_index(
            "Frame"
        )


        st.line_chart(
            headlight_chart,
            use_container_width=True
        )


        # ====================================================
        # GRAPH 4
        # ====================================================

        st.subheader(
            "Adaptive Beam Intensity vs Frame"
        )


        beam_chart = df[
            [
                "Frame",
                "Beam Intensity"
            ]
        ].set_index(
            "Frame"
        )


        st.line_chart(
            beam_chart,
            use_container_width=True
        )


        # ====================================================
        # GRAPH 5
        # ====================================================

        st.subheader(
            "Glare Level Distribution"
        )


        glare_distribution = (
            df["Glare Level"]
            .value_counts()
            .reindex(
                [
                    "LOW",
                    "MEDIUM",
                    "HIGH"
                ],
                fill_value=0
            )
        )


        st.bar_chart(
            glare_distribution,
            use_container_width=True
        )


        # ====================================================
        # GRAPH 6
        # ====================================================

        st.subheader(
            "Average System Parameters"
        )


        average_data = pd.DataFrame(
            {
                "Average Value": [
                    df["Vehicles"].mean(),
                    df["Approaching Vehicles"].mean(),
                    df["Headlights"].mean(),
                    df["Glare Score"].mean(),
                    df["Beam Intensity"].mean()
                ]
            },
            index=[
                "Vehicles",
                "Approaching Vehicles",
                "Headlights",
                "Glare Score",
                "Beam Intensity"
            ]
        )


        st.bar_chart(
            average_data,
            use_container_width=True
        )


        # ====================================================
        # CSV DOWNLOAD
        # ====================================================

        st.divider()

        st.subheader(
            "CSV Report"
        )


        with open(
            csv_path,
            "rb"
        ) as csv_file:

            csv_bytes = (
                csv_file.read()
            )


        st.download_button(
            label="DOWNLOAD CSV REPORT",
            data=csv_bytes,
            file_name=os.path.basename(
                csv_path
            ),
            mime="text/csv",
            use_container_width=True
        )


        # ====================================================
        # CSV TABLE
        # ====================================================

        st.subheader(
            "Detection Data"
        )


        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Anti-Glare Headlight System | "
    "Computer Vision Based Adaptive Headlight Control"
)