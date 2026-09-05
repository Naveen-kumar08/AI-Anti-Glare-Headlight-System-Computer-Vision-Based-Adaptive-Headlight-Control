def determine_beam_action(
    glare_level
):

    if glare_level == "HIGH":

        return {
            "action":
                "HIGH GLARE - DIM AND REDIRECT",

            "beam_intensity":
                30,

            "beam_angle":
                "DOWNWARD"
        }

    elif glare_level == "MEDIUM":

        return {
            "action":
                "MEDIUM GLARE - REDUCE BEAM",

            "beam_intensity":
                60,

            "beam_angle":
                "SLIGHTLY DOWNWARD"
        }

    else:

        return {
            "action":
                "NORMAL BEAM",

            "beam_intensity":
                100,

            "beam_angle":
                "NORMAL"
        }