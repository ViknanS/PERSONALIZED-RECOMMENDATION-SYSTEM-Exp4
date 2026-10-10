"""Saving the recommendation results to a file."""

import datetime
import os

import utils


def save(profile, items, verbose=True):
    """Write the ranked recommendations to outputs/recommendations.txt."""
    ranked = sorted(items, key=lambda i: i["score"], reverse=True)
    lines = [
        "PERSONALIZED RECOMMENDATIONS",
        "=" * 50,
        "User       : {}".format(profile["name"]),
        "Background : {}".format(profile["background"]),
        "Interests  : {}".format(profile["interests"]),
        "Skill Level: {}".format(profile["skill_level"]),
        "Goal       : {}".format(profile["goal"]),
        "Generated  : {}".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")),
        "=" * 50,
        "",
    ]
    for rank_no, item in enumerate(ranked, 1):
        lines += ["{}. {}".format(rank_no, item["name"]),
                  "   Score  : {}%".format(item["score"]),
                  "   Reason : {}".format(item["reason"]), ""]

    try:
        os.makedirs(utils.OUTPUT_DIR, exist_ok=True)
        with open(utils.RECOMMENDATION_FILE, "w") as f:
            f.write("\n".join(lines))
    except OSError as exc:
        raise utils.ModelError("Could not save the recommendations: {}".format(exc))

    if verbose:
        print("Recommendation saved successfully.")
        print("File            : {}".format(utils.RECOMMENDATION_FILE))
        print("Recommendations : {}".format(len(ranked)))
        print("Characters      : {}".format(len("\n".join(lines))))
    return utils.RECOMMENDATION_FILE


if __name__ == "__main__":
    utils.banner("SAVE RECOMMENDATIONS")
    p = utils.require_profile()
    r = utils.require_recommendations()
    if p and r:
        save(p, r["items"])
