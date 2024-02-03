from flask import Flask, render_template, jsonify, request,url_for
import requests

app = Flask(__name__,static_url_path='/static')

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
            return render_template('thumbnails.html', thumbnails=thumbnails)

        else:
            return jsonify({"error": "Invalid JSON structure. 'ott_recommendations' or 'contents' key not found."})

    except requests.exceptions.RequestException as error:
        return jsonify({"error": str(error)})
    
PIXEL_API = "https://cla-pixel.lgads.tv/pixels"
EPG_STATION_API = "hhttps://cla-epg.lgads.tv/epg/listings?"

from datetime import datetime

# Define HEADERS with Authorization if not already defined
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer XBhcf1SFv"
}

# @app.route("/<deviceID>")
@app.route("/get_top_p")
def get_top_programs():
    deviceID = 'acce6f81ed8c63ab308bb915725e2886'
    params = {"deviceId": deviceID}
    pixel_response = requests.get(PIXEL_API, headers=HEADERS, params=params)
    pixel_response.raise_for_status()
    pixel_data = pixel_response.json()
    station_ids_set = set()  # Set to keep track of unique station IDs

    for pixel_entry in pixel_data:
        station_id = pixel_entry["stationId"]
        station_ids_set.add(station_id)

        if len(station_ids_set) >= 1:
            break  

    station_genres = set()

    for entry in station_ids_set:
        print(1)

        response = requests.get(
            EPG_STATION_API,
            params={
                "src": "tms",
                "stationId": entry,
            },
            headers=HEADERS
        )

        response.raise_for_status()
        data = response.json()
        # print(data)
        for program in data['result']:
            genre = program['programInfo']['genre']
            station_genres.update(genre)

        # Convert set of genres to a list
        station_genres_list = list(station_genres)

        # Make a request to the external API
        external_response = requests.get(API_URL, headers=HEADERS)
        external_response.raise_for_status()
        external_data = external_response.json()  # Assuming external_data is JSON

        # Filter results based on genres obtained
        search_rating = float(request.args.get('rating', 0.0))
        filtered_data = sorted(
            (video for video in external_data['ott_recommendations']['contents']
             if any(genre in video.get('genre', []) for genre in station_genres_list) and video.get('rating', 0.0) >= search_rating),
            key=lambda x: x['rating'],
            reverse=True
        )[:10]
        
        # thumbnails = [video.get("thumbnail") for video in filtered_data]
        # return render_template('thumbnails.html', thumbnails=thumbnails)

        return jsonify(filtered_data)
    
OTT_SEARCH_API = "https://cla-epg.lgads.tv/epg/ott/search"

@app.route("/")
def search_ott():
    # Retrieve the search query from the request
    search_query = "King Lear"
    # search_query = request.args.get("search")

    if not search_query:
        return jsonify({"error": "Search query is required"}), 400

    # Make a request to the OTT Search API
    ott_response = requests.get(OTT_SEARCH_API, params={"search": search_query}, headers=HEADERS)

    ott_data = ott_response.json()
        
        # Get the first 10 results
    ott_results = ott_data['result']['result'][:10]

        # Return the first 10 results as JSON
    print(ott_results)
    return jsonify({"result": ott_results})


if __name__ == "__main__":
    app.run(debug=True)