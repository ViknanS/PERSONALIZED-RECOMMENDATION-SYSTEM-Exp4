"""Part A / B - User profile handling and preference analysis (Q2, Q3)."""

import utils


def show_profile(profile):
    """Display the stored user profile."""
    print("USER PROFILE")
    print(utils.DASH)
    for label, key in [("Name", "name"), ("Age", "age"), ("Background", "background"),
                       ("Interests", "interests"), ("Skill Level", "skill_level"),
                       ("Preferred Type", "category"), ("Goal", "goal"),
                       ("No. of Items", "count")]:
        print("{:<16}: {}".format(label, profile[key]))
    print(utils.DASH)


def analyse_preferences(profile, verbose=True):
    """Q3 - identify major interests, skill level, goal, preferred type and constraints."""
    interests = [i.strip() for i in profile["interests"].split(",") if i.strip()]
    analysis = {
        "primary_interest": interests[0] if interests else profile["interests"],
        "secondary_interest": interests[1] if len(interests) > 1 else "-",
        "skill_level": profile["skill_level"],
        "goal": profile["goal"],
        "preference": profile["category"],
        "constraints": "Content must suit a {} learner aiming to {}".format(
            profile["skill_level"].lower(), profile["goal"].lower()),
    }

    if verbose:
        print("Preference Analysis")
        print(utils.DASH)
        print("Primary Interest   : {}".format(analysis["primary_interest"]))
        print("Secondary Interest : {}".format(analysis["secondary_interest"]))
        print("Skill Level        : {}".format(analysis["skill_level"]))
        print("Goal               : {}".format(analysis["goal"]))
        print("Preference         : {}".format(analysis["preference"]))
        print("Constraints        : {}".format(analysis["constraints"]))
        print(utils.DASH)
    return analysis


if __name__ == "__main__":
    utils.banner("PREFERENCE ANALYSIS")
    p = utils.require_profile()
    if p:
        analyse_preferences(p)
