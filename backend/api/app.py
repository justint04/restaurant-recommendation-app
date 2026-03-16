from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.scripts.data_pipeline import run_location_search

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
    app.run(debug=True, port=5000)

    