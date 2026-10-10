"""Part I - Complete Personalized Recommendation System (Q10).

Menu driven application with continuous interaction until the user exits.
Free text requests are routed by the intent detector.
"""

import explanation_module
import feedback_module
import input_module
import intent_module
import profile_module
import prompt_module
import ranking_module
import recommendation_module
import save_module
import utils

MENU = """  1. Enter User Profile
  2. Show Preference Analysis
  3. Generate Recommendations
  4. Rank Recommendations
  5. Explain Recommendations
  6. Give Feedback and Refine
  7. Save Recommendations
  8. Detect Intent of a Request
  9. Exit"""


def home_screen():
    print(utils.LINE)
    print("          PERSONALIZED RECOMMENDATION SYSTEM")
    print("          Powered by {} running locally on Ollama".format(utils.OLLAMA_MODEL))
    print(utils.LINE)
    print(MENU)
    print(utils.LINE)


def do_generate(profile):
    analysis = profile_module.analyse_preferences(profile, verbose=False)
    recommendation_module.generate(profile, analysis)


def route(intent, profile):
    """Run the action that matches a detected intent."""
    if intent == "SHOW_PROFILE":
        profile_module.show_profile(profile)
    elif intent == "GENERATE_RECOMMENDATION":
        do_generate(profile)
    elif intent == "REFINE_RECOMMENDATION":
        if utils.require_recommendations():
            feedback_module.refine(input("Your feedback : ").strip(), profile)
    elif intent == "EXPLAIN_RECOMMENDATION":
        result = utils.require_recommendations()
        if result:
            explanation_module.explain(result["items"], profile)
    elif intent == "SAVE_RECOMMENDATION":
        result = utils.require_recommendations()
        if result:
            save_module.save(profile, result["items"])
    elif intent == "EXIT":
        print("Thank you for using the Personalized Recommendation System. Goodbye!")
        return False
    return True


def handle(choice):
    if choice == "1":
        input_module.display_profile(input_module.collect_profile())
        return True

    profile = utils.require_profile()
    if not profile:
        return True

    if choice == "2":
        profile_module.analyse_preferences(profile)
    elif choice == "3":
        do_generate(profile)
    elif choice == "4":
        result = utils.require_recommendations()
        if result:
            ranking_module.rank(result["items"])
    elif choice == "5":
        result = utils.require_recommendations()
        if result:
            explanation_module.explain(result["items"], profile)
    elif choice == "6":
        if utils.require_recommendations():
            feedback_module.refine(input("Which recommendations are useful? : ").strip(),
                                   profile)
    elif choice == "7":
        result = utils.require_recommendations()
        if result:
            save_module.save(profile, result["items"])
    elif choice == "8":
        request = input("Enter your request : ").strip()
        if not request:
            print("Request cannot be empty.")
            return True
        intent = intent_module.detect_intent(request)
        print()
        print("Detected Intent : {}".format(intent))
        print(utils.DASH)
        return route(intent, profile)
    else:
        print("Invalid choice. Please enter a number between 1 and 9.")
    return True


def main():
    try:
        utils.check_model()
    except utils.ModelError as exc:
        print(utils.LINE)
        print("  PERSONALIZED RECOMMENDATION SYSTEM")
        print(utils.LINE)
        print(exc)
        return

    home_screen()

    while True:
        try:
            choice = input("Enter your choice : ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not choice:
            continue
        if choice == "9" or choice.lower() == "exit":
            print("\nThank you for using the Personalized Recommendation System. Goodbye!")
            break

        print()
        try:
            if not handle(choice):
                break
        except utils.ModelError as exc:
            print("Error: {}".format(exc))
        print(utils.LINE)


if __name__ == "__main__":
    main()
