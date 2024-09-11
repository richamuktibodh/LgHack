from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_URL = "https://cla-recommendation.lgads.tv/recommendation/popular?type=ott"
BEARER_TOKEN = "ZxPgKlOxZ"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

# @app.route("/")
# def index():
#     try:
#         response = requests.get(API_URL, headers=HEADERS)
#         response.raise_for_status()  # Raises HTTPError for bad responses

#         data = response.json()

#         # Check if 'ott_recommendations' and 'contents' keys exist in data
#         if 'ott_recommendations' in data and 'contents' in data['ott_recommendations']:
#             search_rating = float(request.args.get('rating', 0.0))
#             search_genre='Drama'
#             filtered_data = sorted(
#                 (video for video in data['ott_recommendations']['contents']
#                  if search_genre in video.get('genre', []) and video.get('rating', 0.0) >= search_rating),
#                 key=lambda x: x['rating'],
#                 reverse=True
#             )[:10]
#             return jsonify(filtered_data)

#         else:
#             return jsonify({"error": "Invalid JSON structure. 'ott_recommendations' or 'contents' key not found."})

#     except requests.exceptions.RequestException as error:
#         return jsonify({"error": str(error)})

# PIXEL_API = "https://cla-pixel.lgads.tv/pixels"
# EPG_STATION_API = "hhttps://cla-epg.lgads.tv/epg/listings?"

# from datetime import datetime

# PIXEL_API = "https://cla-pixel.lgads.tv/pixels"
# EPG_STATION_API = " https://cla-epg.lgads.tv/epg/listings?"

# # Define HEADERS with Authorization if not already defined
# HEADERS = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer XBhcf1SFv"
# }

# @app.route("/get_top_p")
# def get_top_programs():
#     device_id = 'acce6f81ed8c63ab308bb915725e2886'
#     params = {"deviceId": device_id}
#     pixel_response = requests.get(PIXEL_API, headers=HEADERS, params=params)
#     pixel_response.raise_for_status()
#     pixel_data = pixel_response.json()
#     station_ids_set = set()  # Set to keep track of unique station IDs

#     for pixel_entry in pixel_data:
#         station_id = pixel_entry["stationId"]
#         station_ids_set.add(station_id)

#         if len(station_ids_set) >= 1:
#             break  

#     station_genres = set()

#     for entry in station_ids_set:
#         response = requests.get(
#             EPG_STATION_API,
#             params={
#                 "src": "tms",
#                 "stationId": entry,
#             },
#             headers=HEADERS
#         )

#         response.raise_for_status()
#         data = response.json()
#         # print(data)
#         for program in data['result']:
#             genre = program['programInfo']['genre']
#             station_genres.update(genre)

#         # Convert set of genres to a list
#         station_genres_list = list(station_genres)

#         # Make a request to the external API
#         external_response = requests.get(API_URL, headers=HEADERS)
#         external_response.raise_for_status()
#         external_data = external_response.json()  # Assuming external_data is JSON

#         # Filter results based on genres obtained
#         search_rating = float(request.args.get('rating', 0.0))
#         filtered_data = sorted(
#             (video for video in external_data['ott_recommendations']['contents']
#              if any(genre in video.get('genre', []) for genre in station_genres_list) and video.get('rating', 0.0) >= search_rating),
#             key=lambda x: x['rating'],
#             reverse=True
#         )[:10]

#         return jsonify(filtered_data)

# bookmarks = {}
# @app.route("/bookmark", methods=["POST"])
# def bookmark_click():
#     # Retrieve device ID and click ID from the request
#     device_id = request.json.get("device_id")
#     click_id = request.json.get("click_id")

#     if not device_id or not click_id:
#         return jsonify({"error": "Device ID and Click ID are required"}), 400

#     # Check if the device_id is already in the bookmarks dictionary
#     if device_id not in bookmarks:
#         bookmarks[device_id] = []

#     # Add the click_id to the vector for the given device_id
#     bookmarks[device_id].append(click_id)

#     return jsonify({"message": "Click bookmarked successfully"})


# @app.route("/bookmarks/<int:device_id>")
# def get_bookmarks(device_id):
#     # Retrieve bookmarks for a specific device_id
#     if device_id not in bookmarks:
#         return jsonify({"message": "No bookmarks found for the device"}), 404

#     device_bookmarks = bookmarks[device_id]
#     return jsonify({"device_id": device_id, "bookmarks": device_bookmarks})


# OTT_SEARCH_API = "https://cla-epg.lgads.tv/epg/ott/search"

# @app.route("/")
# def search_ott():
#     # Retrieve the search query from the request
#     search_query = "King Lear"
#     # search_query = request.args.get("search")

#     if not search_query:
#         return jsonify({"error": "Search query is required"}), 400

#     # Make a request to the OTT Search API
#     ott_response = requests.get(OTT_SEARCH_API, params={"search": search_query}, headers=HEADERS)

#     ott_data = ott_response.json()
        
#         # Get the first 10 results
#     ott_results = ott_data['result']['result'][:10]

#         # Return the first 10 results as JSON
#     print(ott_results)
#     return jsonify({"result": ott_results})


# if __name__ == "__main__":
#     app.run(debug=True)


