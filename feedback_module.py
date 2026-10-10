"""Part G - User feedback and recommendation refinement (Q8)."""

import profile_module
import recommendation_module
import utils


def refine(feedback, profile, verbose=True):
    """Q8 - regenerate the recommendation list taking the feedback into account."""
    previous = utils.load_result()
    old_names = [i["name"] for i in previous["items"]] if previous else []

    extra = ("The user gave this feedback on the previous recommendations:\n"
             "\"{}\"\n"
             "Previously suggested: {}\n"
             "Apply the feedback strictly. Remove anything the user rejected and "
             "favour what the user prefers.").format(feedback, ", ".join(old_names) or "none")

    analysis = profile_module.analyse_preferences(profile, verbose=False)

    if verbose:
        print("User Feedback")
        print(utils.DASH)
        print(feedback)
        print(utils.DASH)
        print()
        print("Refining recommendations ...")
        print()

    result = recommendation_module.generate(profile, analysis, verbose=False, extra=extra)
    if verbose:
        recommendation_module.display(result["items"], "REFINED RECOMMENDATIONS")
    return result


if __name__ == "__main__":
    utils.banner("USER FEEDBACK AND REFINEMENT")
    p = utils.require_profile()
    r = utils.require_recommendations()
    if p and r:
        refine(input("Which recommendations are useful? : ").strip(), p)
