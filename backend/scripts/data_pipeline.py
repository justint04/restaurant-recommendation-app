import os
import traceback
from dotenv import load_dotenv
from backend.api.google_client import get_place_info, get_place_details, search_restaurants_by_location
from backend.database.db_connection import get_connection
from backend.processing.text_processor import process_text
from backend.processing.scorer import score_review_by_category, score_restaurant_by_category

load_dotenv()
#for now i am using address as my input, however it should be through my react website
#when i code it 
api_key = os.getenv("GOOGLE_PLACES_API_KEY")
address = "Rubys Cafe SOHO"

#this function runs the data pipeline

def run_pipeline(address):
    print("start pipeline")
    
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found in environment")
        return
    
    #get a place_info api request and store the information
    place_info = get_place_info(address, api_key)
    if not place_info:
        print("ERROR: Failed to get place info- check API KEY or address")
        return
    print(f"place_info: {place_info}")

    #get a place_details api request and store the information
    place_id = place_info["place_id"]
    place_details = get_place_details(place_id, api_key)

    if not place_details:
        print("Failed to get place details")
        return
    
    print(f"place_details: {place_details}")
    #connect to postgresql database and insert it into restaurants table
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO restaurants (
                place_id,
                name,
                address,
                rating,
                business_status,
                formatted_address,
                editorial_summary,
                price_level,
                url,
                serves_vegetarian_food
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (place_id) DO UPDATE SET
            name = EXCLUDED.name,
            address = EXCLUDED.address,
            rating = EXCLUDED.rating
       """,
       (
           place_id,
           place_details.get("name"),
           place_info.get("address"),
           place_details.get("rating"),
           place_details.get("business_status"),
           place_details.get("formatted_address"),
           place_details.get("editorial_summary"),
           place_details.get("price_level"),
           place_details.get("url"),
           place_details.get("serves_vegetarian_food"),
       )
        )

        #extract reviews from place details api call
        reviews = place_details.get("reviews") or []
        all_review_scores = []

        #for every review in our reviews, process the text into keywords and score each review
        for review in reviews:
            words = process_text(review.get("text") or "")
            scores = score_review_by_category(words)
            all_review_scores.append(scores)
            print(f"{review.get('author_name')}: {scores}")

        #insert information that comes with each review into our reviews table
            cur.execute(
                """
                INSERT INTO reviews (
                    place_id,
                    author_name,
                    rating,
                    text,
                    translated,
                    score_food,
                    score_service,
                    score_ambiance,
                    score_value,
                    score_total
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    place_id,
                    review.get("author_name"),
                    review.get("rating"),
                    review.get("text"),
                    review.get("translated"),
                    scores["food"],
                    scores["service"],
                    scores["ambiance"],
                    scores["value"],
                    scores["total"],
                )
            )

        #score all the restaurants by category and store in restaurant_scores
        restaurant_scores = score_restaurant_by_category(all_review_scores) 

        #commit the inserts into our database
        conn.commit()
        print(f"Inserted restaurant and {len(reviews)} reviews")
        print(f"Restaurant scores: {restaurant_scores}")
    
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        traceback.print_exc()
        conn.rollback()

    finally:
        print("Data inserted successfully")
        cur.close()
        conn.close()
                
def run_location_search(query):
    #Pipeline for location based search such as "pasta near nyc"
    print(f"Searching for: {query}")

    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found in environment")
        return []
    
    places = search_restaurants_by_location(query, api_key)
    if not places:
        print("No results found")
        return []
    
    results = []

    for place in places:
        place_id = place["place_id"]
        print(f"Getting details for: {place['name']}")

        place_details = get_place_details(place_id, api_key)
        if not place_details:
            print(f"Skipping {place['name']} - could not get details")
            continue

        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO restaurants (
                    place_id,
                    name,
                    address,
                    rating,
                    business_status,
                    formatted_address,
                    editorial_summary,
                    price_level,
                    url,
                    serves_vegetarian_food
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (place_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    address = EXCLUDED.address,
                    rating = EXCLUDED.rating
                """, 
                (
                    place_id,
                    place_details.get("name"),
                    place_details.get("formatted_address"),
                    place_details.get("rating"),
                    place_details.get("business_status"),
                    place_details.get("editorial_summary"),
                    place_details.get("price_level"),
                    place_details.get("url"),
                    place_details.get("serves_vegetarian_food"),
                )
            )

            reviews = place_details.get("reviews", [])
            all_review_scores = []

            for review in reviews:
                words = process_text(review.get("text") or "")
                scores = score_review_by_category(words)
                all_review_scores.append(scores)

                cur.execute(
                    """
                    INSERT INTO reviews (
                        place_id,
                        author_name,
                        rating,
                        text,
                        translated,
                        score_food,
                        score_service,
                        score_ambiance,
                        score_value,
                        score_total
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (
                        place_id,
                        review.get("authorAttribution", {}).get("displayName"),
                        review.get("rating"),
                        review.get("text", {}).get("text"),
                        review.get("translated"),
                        scores["food"],
                        scores["service"],
                        scores["ambiance"],
                        scores["value"],
                        scores["total"],
                    )
                )

                restaurant_scores = score_restaurant_by_category(all_review_scores)
                conn.commit()
                print(f"Inserted {place_details.get('name')} with {len(reviews)} reviews")

                results.append({
                    "name": place_details.get("name"),
                    "address": place_details.get("formatted_address"),
                    "rating": place_details.get("rating"),
                    "scores": restaurant_scores
                })

        except Exception as e:
            print(f"DATABASE ERROR for {place['name']}: {e}")
            traceback.print_exc()
            conn.rollback()
        finally:
            cur.close()
            conn.close()

    results.sort(key=lambda x: x["scores"]["total"], reverse=True)
    print(f"\nFinal ranked results:")
    for i, r in enumerate(results):
        print(f"#{i+1} {r['name']} - Total score: {r['scores']['total']}")
    
    return results

if __name__ == "__main__":
    run_location_search("coffee shops soho nyc")

#run using python -m backend.scripts.data_pipeline

