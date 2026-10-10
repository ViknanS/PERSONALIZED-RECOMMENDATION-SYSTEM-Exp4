"""Part E - Recommendation ranking (Q6)."""

import utils


def rank(items, verbose=True):
    """Q6 - rank the recommendations by suitability score."""
    ranked = sorted(items, key=lambda i: i["score"], reverse=True)

    if verbose:
        width = max([len(i["name"]) for i in ranked] + [14])
        print("RECOMMENDATION RANKING")
        print(utils.DASH)
        print("{:<5} | {:<{w}} | {}".format("Rank", "Recommendation", "Score", w=width))
        print("-" * (width + 20))
        for rank_no, item in enumerate(ranked, 1):
            print("{:<5} | {:<{w}} | {}%".format(rank_no, item["name"], item["score"], w=width))
        print("-" * (width + 20))
    return ranked


if __name__ == "__main__":
    utils.banner("RECOMMENDATION RANKING")
    r = utils.require_recommendations()
    if r:
        rank(r["items"])
