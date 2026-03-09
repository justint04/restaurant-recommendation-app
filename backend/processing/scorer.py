#small list of positive keywords for now, add more as we go and potentially load it in postgresql instead
POSITIVE_KEYWORDS = {
    "delicious", "amazing", "great", "fresh", "friendly",
    "cozy", "perfect", "loved", "excellent", "tasty"
}
#small list of negative keywords for now, add more as we go and potentially load it in postgresql instead

NEGATIVE_KEYWORDS = {
    "bad", "awful", "rude", "slow", "disgusting",
    "overpriced", "cold", "wrong", "disappointed", "hostile"
}

#words is an array of relevant keywords from text_processor 
#this compares every word in words to our list of negative and positive keywords
#+1 for each positive, +1 for each negative

def score_review(words):
    score = 0
    for word in words:
        if word in POSITIVE_KEYWORDS:
            score += 1
        elif word in NEGATIVE_KEYWORDS:
            score -= 1
        return score
    
#this sums each review's scores, since each restaurant has 5 reviews
def score_restaurant(reviews):  
    if not reviews:
        return 0
    total = sum(score_review(review) for review in reviews)
    return total / len(reviews)


        