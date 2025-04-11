import requests
from flask import current_app

class MapService:
    @staticmethod
    def get_nearby_exhibitions(lat, lng, radius=5000):
        """
        Uses Google Places API to get nearby art galleries and museums based on the given latitude and longitude.
        """

        API_KEY = current_app.config["GOOGLE_PLACES_API_KEY"]

        if not API_KEY:
            return {"error": "Google API key not set"}, 500
        

        # Field Mask options:
        # id, displayName, formattedAddress, location, types, primaryType, rating, userRatingCount,
        # priceLevel, businessStatus, regularOpeningHours, photos, googleMapsUri, websiteUri, editorialSummary, reviews


        url = "https://places.googleapis.com/v1/places:searchNearby"
        headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.rating,places.websiteUri,places.googleMapsUri,places.editorialSummary"
        }
        payload = {
            "includedTypes": ["art_gallery", "museum"],
            "maxResultCount": 10,
            "locationRestriction": {
                "circle": {
                    "center": {"latitude": float(lat), "longitude": float(lng)},
                    "radius": 5000.0 
                }
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()


            exhibitions = [
                {
                    "name": place.get("displayName", {}).get("text", "Unknown"),
                    "address": place.get("formattedAddress", "No address available"),
                    "latitude": place.get("location", {}).get("latitude"),
                    "longitude": place.get("location", {}).get("longitude"),
                    "rating": place.get("rating", "N/A"),
                    "website": place.get("websiteUri", "Not available"),
                    "gmaps": place.get("googleMapsUri", {}),
                    "directions_link": f"https://www.google.com/maps/dir/?api=1&destination={place.get("location", {}).get("latitude")},{place.get("location", {}).get("longitude")}&origin={lat},{lng}",
                    "summary": place.get("editorialSummary", {}),
                    "id": place.get("id")
                }
                for place in data.get("places", [])
            ]

            return exhibitions, 200

        except Exception as e:
            return {"error": f"Failed to fetch exhibitions: {str(e)}"}, 500