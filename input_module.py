"""Part A - User profile collection (Q1, Q2)."""

import utils

FIELDS = [
    ("name", "Name                      : ", "Student"),
    ("age", "Age                       : ", "20"),
    ("background", "Educational Background    : ", "Computer Science"),
    ("interests", "Interests                 : ", "Artificial Intelligence, Python"),
    ("skill_level", "Skill Level               : ", "Beginner"),
    ("category", "Preferred Category        : ", "Online Courses"),
    ("goal", "Goal                      : ", "Learn AI"),
]


def collect_profile():
    """Q1 - read the user's details."""
    print("Enter Your Details")
    print(utils.DASH)

    profile = {}
    for key, prompt, default in FIELDS:
        value = input(prompt).strip()
        if not value and key == "name":
            while not value:
                print("Name cannot be empty.")
                value = input(prompt).strip()
        profile[key] = value or default

    count = None
    while count is None:
        raw = input("Number of Recommendations : ").strip()
        if not raw:
            count = 5
        elif raw.isdigit() and 1 <= int(raw) <= 10:
            count = int(raw)
        else:
            print("Please enter a whole number between 1 and 10.")
    profile["count"] = count

    utils.save_profile(profile)
    return profile


def display_profile(profile):
    """Q2 - display the collected information neatly."""
    print()
    print(utils.DASH)
    print("COLLECTED USER PROFILE")
    print(utils.DASH)
    print("Name            : {}".format(profile["name"]))
    print("Age             : {}".format(profile["age"]))
    print("Background      : {}".format(profile["background"]))
    print("Interests       : {}".format(profile["interests"]))
    print("Skill Level     : {}".format(profile["skill_level"]))
    print("Preferred Type  : {}".format(profile["category"]))
    print("Goal            : {}".format(profile["goal"]))
    print("No. of Items    : {}".format(profile["count"]))
    print(utils.DASH)


if __name__ == "__main__":
    utils.banner("USER PROFILE COLLECTION")
    display_profile(collect_profile())
