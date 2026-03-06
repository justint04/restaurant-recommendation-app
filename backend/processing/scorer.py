POSITIVE_KEYWORDS = {
    "delicious", "amazing", "great", "fresh", "friendly",
    "cozy", "perfect", "loved", "excellent", "tasty"
}

NEGATIVE_KEYWORDS = {
    "bad", "awful", "rude", "slow", "disgusting",
    "overpriced", "cold", "wrong", "disappointed", "hostile"
}

def score_review(words):
    score = 0

    for word in words:
        if word in POSITIVE_KEYWORDS:
            score += 1
        elif word in NEGATIVE_KEYWORDS:
            score -= 1
        return score

def score_restaurant(reviews):  
    if not reviews:
        return 0
    total = sum(score_review(review) for review in reviews)
    return total / len(reviews)


        