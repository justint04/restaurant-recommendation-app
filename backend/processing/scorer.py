#list of positive and negative keywords based on category
#can already see issues with this as someone can put "not worth" and it may be scored positively, will have to fix this later

CATEGORY_KEYWORDS = {
    "food": {
        #positive 
        "delicious": 1, "tasty": 1, "fresh": 1, "amazing": 1, "flavorful": 1, "perfect": 1,
        "yummy": 1, "cooked": 1, "crispy": 1, "juicy": 1,
        #negative
        "nasty": -1, "bland": -1, "cold": -1, "stale": -1, "overcooked": -1, "undercooked": -1,
        "soggy": -1, "awful": -1, "disgusting": -1, "sick": -1,
    },
    
    "service": {
        #positive
        "friendly": 1, "attentive": 1, "fast": 1, "helpful": 1, "welcoming": 1, "professional": 1,
        "kind": 1, "efficient": 1, "courteous": 1,

        #negative
        "rude": -1, "slow": -1, "hostile": -1, "ignored": -1, "attitude": -1, "unfriendly": -1,
        "inattentive": -1, "unprofessional": -1,
    },

    "ambiance": {
        #positive
        "cozy": 1, "vibe": 1, "atmosphere": 1, "beautiful": 1, "charming": 1, "clean": 1,
        "comfortable": 1, "cute": 1, "lovely": 1, "aesthetic": 1,

        #negative
        "loud": -1, "crowded": -1, "dirty": -1, "cramped": -1, "noisy": -1, "uncomfortable": -1,
        "chaotic": -1, "dark": -1,
    },

    "value": {
        #positive
        "worth": 1, "affordable": 1, "reasonable": 1, "generous": 1, "deal": 1, "cheap": 1, "bargain": 1,

        #negative
        "overpriced": -1, "expensive": -1, "pricey": -1, "charged": -1, "steep": -1, "costly": -1,
    }

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


        