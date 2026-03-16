from flask import Flask, jsonify, request
from backend.scripts.data_pipeline import run_location_search

app = Flask(__name__)

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")
    results = run_location_search("query")
    return jsonify(results)
    