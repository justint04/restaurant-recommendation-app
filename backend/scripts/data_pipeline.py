import os
import traceback
from dotenv import load_dotenv
from backend.api.google_client import get_place_info, get_place_details
from backend.database.db_connection import get_connection

load_dotenv()

api_key = os.getenv("GOOGLE_PLACES_API_KEY")
address = "Rubys Cafe SOHO"

def run_pipeline(address):
    print("start pipeline")
    
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found in environment")
        return
    
    place_info = get_place_info(address, api_key)
    if not place_info:
        print("ERROR: Failed to get place info- check API KEY or address")
        return
    print(f"place_info: {place_info}")

    place_id = place_info["place_id"]
    place_details = get_place_details(place_id, api_key)

    if not place_details:
        print("Failed to get place details")
        return
    
    print(f"place_details: {place_details}")

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

        reviews = place_details.get("reviews") or []
        for review in reviews:
            cur.execute(
                """
                INSERT INTO reviews (
                    place_id,
                    author_name,
                    rating,
                    text,
                    translated
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    place_id,
                    review.get("author_name"),
                    review.get("rating"),
                    review.get("text"),
                    review.get("translated")
                )
            )
        conn.commit()
        print(f"Inserted restaurant and {len(reviews)} reviews")
    
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        traceback.print_exc()
        conn.rollback()

    finally:
        print("Data inserted successfully")
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_pipeline(address)

#run using python -m backend.scripts.data_pipeline
#for now we will use address but it should be input from a website in the future
