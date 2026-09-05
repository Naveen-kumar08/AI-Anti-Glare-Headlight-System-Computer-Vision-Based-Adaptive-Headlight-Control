def calculate_glare_score(
    headlights,
    approaching=False
):

    if not headlights:

        return {
            "score": 0,
            "level": "LOW"
        }

    maximum_brightness = max(
        light["brightness"]
        for light in headlights
    )

    total_area = sum(
        light["area"]
        for light in headlights
    )

    brightness_score = (
        maximum_brightness / 255
    ) * 60

    area_score = min(
        total_area / 500,
        1
    ) * 20

    approaching_score = (
        20
        if approaching
        else 0
    )

    score = (
        brightness_score
        +
        area_score
        +
        approaching_score
    )

    score = min(
        round(score),
        100
    )

    if score >= 70:

        level = "HIGH"

    elif score >= 40:

        level = "MEDIUM"

    else:

        level = "LOW"

    return {
        "score": score,
        "level": level
    }