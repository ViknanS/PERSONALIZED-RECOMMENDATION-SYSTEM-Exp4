"""Part H - Intelligent intent detection (Q9)."""

import utils

INTENTS = ("GENERATE_RECOMMENDATION", "REFINE_RECOMMENDATION", "SHOW_PROFILE",
           "EXPLAIN_RECOMMENDATION", "SAVE_RECOMMENDATION", "EXIT")

SYSTEM = (
    "You are an intent classifier for a personalized recommendation system.\n"
    "Reply with exactly one of these labels and nothing else:\n"
    "GENERATE_RECOMMENDATION, REFINE_RECOMMENDATION, SHOW_PROFILE, "
    "EXPLAIN_RECOMMENDATION, SAVE_RECOMMENDATION, EXIT\n\n"
    "GENERATE_RECOMMENDATION - the user wants new recommendations\n"
    "REFINE_RECOMMENDATION   - the user wants the existing list changed or filtered\n"
    "SHOW_PROFILE            - the user wants to see their stored profile\n"
    "EXPLAIN_RECOMMENDATION  - the user asks why something was recommended\n"
    "SAVE_RECOMMENDATION     - the user wants the results written to a file\n"
    "EXIT                    - the user wants to quit\n\n"
    "Examples:\n"
    "Recommend some AI courses. -> GENERATE_RECOMMENDATION\n"
    "Give me more beginner-friendly options. -> REFINE_RECOMMENDATION\n"
    "Why did you recommend this course? -> EXPLAIN_RECOMMENDATION\n"
    "Show my details. -> SHOW_PROFILE\n"
    "Save the results. -> SAVE_RECOMMENDATION\n"
    "I am done. -> EXIT"
)


def detect_intent(query):
    """Q9 - classify the request into exactly one of the six allowed intents."""
    raw = utils.ask(SYSTEM, "User: {}\nLabel:".format(query), temperature=0.0)
    text = raw.upper().replace("-", "_").replace(" ", "_")

    for intent in INTENTS:
        if intent in text:
            return intent
    if "REFINE" in text or "BEGINNER" in text:
        return "REFINE_RECOMMENDATION"
    if "EXPLAIN" in text or "WHY" in text:
        return "EXPLAIN_RECOMMENDATION"
    if "PROFILE" in text:
        return "SHOW_PROFILE"
    if "SAVE" in text:
        return "SAVE_RECOMMENDATION"
    if "EXIT" in text or "QUIT" in text:
        return "EXIT"
    return "GENERATE_RECOMMENDATION"


if __name__ == "__main__":
    utils.banner("INTENT DETECTION  (model: {})".format(utils.OLLAMA_MODEL))
    samples = [
        "Recommend some AI courses.",
        "Give me more beginner-friendly options.",
        "Why did you recommend this course?",
        "Show my details.",
        "Save the results.",
    ]
    print("{:<42} {}".format("User Request", "Detected Intent"))
    print(utils.DASH)
    for q in samples:
        print("{:<42} {}".format(q, detect_intent(q)))
    print(utils.DASH)
