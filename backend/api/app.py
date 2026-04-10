from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.scripts.data_pipeline import run_location_search
import os

#connects python code to html css website
app = Flask(__name__)
CORS(app)

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "query parameter is required"}), 400
    
    results = run_location_search(query)
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    