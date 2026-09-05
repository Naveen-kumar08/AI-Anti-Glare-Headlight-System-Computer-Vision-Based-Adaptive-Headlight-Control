import math


class VehicleTracker:

    def __init__(self):

        self.previous_vehicles = []


    # ========================================================
    # DISTANCE
    # ========================================================

    def calculate_distance(
        self,
        point1,
        point2
    ):

        x1, y1 = point1
        x2, y2 = point2

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )


    # ========================================================
    # FIND PREVIOUS VEHICLE
    # ========================================================

    def find_previous_vehicle(
        self,
        detection
    ):

        best_vehicle = None

        minimum_distance = float(
            "inf"
        )

        for old_vehicle in self.previous_vehicles:

            if (
                old_vehicle["class_name"]
                !=
                detection["class_name"]
            ):
                continue

            distance = self.calculate_distance(
                detection["center"],
                old_vehicle["center"]
            )

            if distance < minimum_distance:

                minimum_distance = distance

                best_vehicle = old_vehicle

        if minimum_distance > 150:

            return None

        return best_vehicle


    # ========================================================
    # CLASSIFY VEHICLE
    # ========================================================

    def classify_vehicle(
        self,
        detection
    ):

        previous = (
            self.find_previous_vehicle(
                detection
            )
        )

        if previous is None:

            return "VEHICLE"

        current_area = (
            detection["width"]
            *
            detection["height"]
        )

        previous_area = (
            previous["width"]
            *
            previous["height"]
        )

        if previous_area <= 0:

            return "VEHICLE"

        size_change = (
            current_area -
            previous_area
        ) / previous_area

        if size_change > 0.08:

            return "APPROACHING"

        return "VEHICLE"


    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        detections
    ):

        classified = []

        for detection in detections:

            direction = (
                self.classify_vehicle(
                    detection
                )
            )

            detection["direction"] = direction

            classified.append(
                detection
            )

        self.previous_vehicles = [
            detection.copy()
            for detection in detections
        ]

        return classified