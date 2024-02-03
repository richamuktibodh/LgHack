from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_URL = "https://cla-recommendation.lgads.tv/recommendation/popular?type=ott"
BEARER_TOKEN = "ZxPgKlOxZ"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

@app.route("/<genre>")
def index(genre):
    genre = genre[0].upper() + genre[1:]
    try:
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.json()

        # Check if 'ott_recommendations' and 'contents' keys exist in data
        if 'ott_recommendations' in data and 'contents' in data['ott_recommendations']:
            search_rating = float(request.args.get('rating', 0.0))
            search_genre= genre
            filtered_data = sorted(
                (video for video in data['ott_recommendations']['contents']
                 if search_genre in video.get('genre', []) and video.get('rating', 0.0) >= search_rating),
                key=lambda x: x['rating'],
                reverse=True
            )[:10]
            thumbnails = [video.get("thumbnail") for video in filtered_data]
            # return jsonify(thumbnails)
            return render_template('thumbnails.html', thumbnails=thumbnails)

        else:
            return jsonify({"error": "Invalid JSON structure. 'ott_recommendations' or 'contents' key not found."})

    except requests.exceptions.RequestException as error:
        return jsonify({"error": str(error)})