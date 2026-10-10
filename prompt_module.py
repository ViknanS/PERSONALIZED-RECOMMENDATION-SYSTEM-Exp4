"""Part C - Prompt construction (Q4)."""

import utils

SYSTEM_PROMPT = ("You are a personalized recommendation assistant. "
                 "Recommend only real, well known resources. "
                 "Return one recommendation per line in exactly this format:\n"
                 "<name> | <score out of 100> | <one sentence reason>\n"
                 "No headings, no numbering, no extra text.")


def build_prompt(profile, analysis):
    """Q4 - construct the prompt from the collected user information."""
    return (
        "User:\n"
        "Name: {name}\n"
        "Background: {background}\n"
        "Interests: {interests}\n"
        "Skill Level: {skill_level}\n"
        "Goal: {goal}\n"
        "Preference: {category}\n\n"
        "Primary Interest: {primary}\n"
        "Constraints: {constraints}\n\n"
        "Recommend {count} suitable learning resources.\n"
        "For each recommendation provide the name, a suitability score out of 100, "
        "and a one sentence reason."
    ).format(primary=analysis["primary_interest"],
             constraints=analysis["constraints"], **profile)


def show_prompt(prompt):
    print("Generated Prompt")
    print(utils.DASH)
    print("[system]")
    print(SYSTEM_PROMPT)
    print()
    print("[user]")
    print(prompt)
    print(utils.DASH)


if __name__ == "__main__":
    import profile_module
    utils.banner("PROMPT GENERATION")
    p = utils.require_profile()
    if p:
        show_prompt(build_prompt(p, profile_module.analyse_preferences(p, verbose=False)))
