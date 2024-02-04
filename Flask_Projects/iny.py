
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
            title = [video.get("title") for video in filtered_data]
            thumbnails = [video.get("thumbnail") for video in filtered_data]
            enumerated_thumbnails = list(enumerate(thumbnails))
            return render_template('thumbnail.html', enumerated_thumbnails=enumerated_thumbnails, title=title)

        else:
            return jsonify({"error": "Invalid JSON structure. 'ott_recommendations' or 'contents' key not found."})

    except requests.exceptions.RequestException as error:
        return jsonify({"error": str(error)})
    
PIXEL_API = "https://cla-pixel.lgads.tv/pixels"
EPG_STATION_API = "https://cla-epg.lgads.tv/epg/listings?"

from datetime import datetime

# Define HEADERS with Authorization if not already defined
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer XBhcf1SFv"
}


# @app.route('/search_action')
# def get_recommendations():
#     print(1)
#     return "Check console for print output"

@app.route('/search_action')
def get_recommendations():
    device_id = request.args.get("deviceID")
    params = {"deviceId": device_id}
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

        titles = [video.get("title") for video in filtered_data]
        print(titles)
        thumbnails = [video.get("thumbnail") for video in filtered_data]
        enumerated_thumbnails = list(enumerate(thumbnails))
        print(enumerated_thumbnails)
        return render_template('thumbnail.html', enumerated_thumbnails=enumerated_thumbnails, title=titles)


OTT_SEARCH_API = "https://cla-epg.lgads.tv/epg/ott/search"

@app.route("/search")
def search_ott():
    print(1)
    # Retrieve the search query from the request
    search_query = request.args.get("g")

    if not search_query:
        return jsonify({"error": "Search query is required"}), 400

    # Make a request to the OTT Search API
    ott_response = requests.get(OTT_SEARCH_API, params={"search": search_query}, headers=HEADERS)

    ott_data = ott_response.json()

    # Extract results from the 'result' key
    ott_results = ott_data.get('result', {}).get('result', [])[:10]
    # print(ott_results)

    # Extract relevant data for thumbnails.html
    titles = [video.get("title") for video in ott_results]
    thumbnails = [video.get("originalImages")[0].get("url") if video.get("originalImages") else None for video in ott_results]
    print(thumbnails)
    enumerated_thumbnails = list(enumerate(thumbnails))
    return render_template('thumbnail.html', enumerated_thumbnails=enumerated_thumbnails, title=titles)


bookmarks = {}
@app.route("/bookmark")
def bookmark_click():
    # Retrieve device ID and click ID from the request
    device_id = request.json.get("device_id")
    click_id = request.json.get("click_id")

    if not device_id or not click_id:
        return jsonify({"error": "Device ID and Click ID are required"}), 400

    # Check if the device_id is already in the bookmarks dictionary
    if device_id not in bookmarks:
        bookmarks[device_id] = []

    # Add the click_id to the vector for the given device_id
    bookmarks[device_id].append(click_id)

    return jsonify({"message": "Click bookmarked successfully"})


@app.route("/bookmarks/<int:device_id>")
def get_bookmarks(device_id):
    # Retrieve bookmarks for a specific device_id
    if device_id not in bookmarks:
        return jsonify({"message": "No bookmarks found for the device"}), 404

    device_bookmarks = bookmarks[device_id]
    return jsonify({"device_id": device_id, "bookmarks": device_bookmarks})



if __name__ == "__main__":
    app.run(debug=True)