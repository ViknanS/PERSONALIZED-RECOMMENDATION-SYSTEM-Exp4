"""Part F - Recommendation explanation (Q7)."""

import utils

SYSTEM = ("You explain why a learning resource suits a particular learner. "
          "Reply with one short sentence only. No preamble, no list markers.")


def explain(items, profile, verbose=True):
    """Q7 - generate an explanation for every recommendation."""
    explanations = []
    for item in items:
        text = utils.ask(SYSTEM,
                         "Learner: {} background, skill level {}, goal {}, interests {}.\n"
                         "Resource: {}\n"
                         "Why does this resource suit the learner?".format(
                             profile["background"], profile["skill_level"],
                             profile["goal"], profile["interests"], item["name"]))
        explanations.append({"name": item["name"], "explanation": text})

    if verbose:
        print("RECOMMENDATION EXPLANATION")
        print(utils.DASH)
        for i, entry in enumerate(explanations, 1):
            print()
            print("{}. {}".format(i, entry["name"]))
            print("   {}".format(entry["explanation"]))
        print()
        print(utils.DASH)
    return explanations


if __name__ == "__main__":
    utils.banner("RECOMMENDATION EXPLANATION")
    r = utils.require_recommendations()
    p = utils.load_profile()
    if r and p:
        explain(r["items"], p)
