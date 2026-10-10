"""Part D - Recommendation generation (Q5)."""

import re

import prompt_module
import utils


def parse_items(reply, limit):
    """Turn the model reply into a list of {name, score, reason}."""
    items = []
    for raw in reply.splitlines():
        line = utils.clean_item(raw)
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        name, score_raw, reason = parts[0], parts[1], " | ".join(parts[2:])
        digits = re.findall(r"\d+", score_raw)
        if not name or not digits:
            continue
        items.append({"name": name, "score": min(int(digits[0]), 100), "reason": reason})
        if len(items) == limit:
            break
    return items


def generate(profile, analysis, verbose=True, extra=""):
    """Q5 - generate personalized recommendations using the model."""
    prompt = prompt_module.build_prompt(profile, analysis)
    if extra:
        prompt += "\n\n" + extra

    reply = utils.ask(prompt_module.SYSTEM_PROMPT, prompt)
    items = parse_items(reply, profile["count"])

    if not items:
        raise utils.ModelError("Could not parse any recommendation from the model reply.")

    result = {"items": items, "profile_name": profile["name"]}
    utils.save_result(result)

    if verbose:
        display(items)
    return result


def display(items, title="PERSONALIZED RECOMMENDATIONS"):
    print(title)
    print(utils.DASH)
    for i, item in enumerate(items, 1):
        print()
        print("{}. {}".format(i, item["name"]))
        print("   Score  : {}%".format(item["score"]))
        print("   Reason : {}".format(item["reason"]))
    print()
    print(utils.DASH)
    print("Recommendations generated : {}".format(len(items)))


if __name__ == "__main__":
    import profile_module
    utils.banner("RECOMMENDATION GENERATION")
    p = utils.require_profile()
    if p:
        generate(p, profile_module.analyse_preferences(p, verbose=False))
