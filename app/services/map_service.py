import requests
import os

class MapService:
    @staticmethod
    def get_nearby_exhibitions(lat, lng, radius=5000):
        """
        Uses Google Places API to get nearby galleries and museums.
        """
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not api_key:
            return {"error": "Google API key not set"}, 500

        location = f"{lat},{lng}"
        types = ["art_gallery", "museum"]
        results = []

        for place_type in types:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": location,
                "radius": radius,
                "type": place_type,
                "key": api_key
            }

            try:
                res = requests.get(url, params=params)
                data = res.json()

                for place in data.get("results", []):
                    results.append({
                        "name": place.get("name"),
                        "place_id": place.get("place_id"),
                        "address": place.get("vicinity"),
                        "type": place_type,
                        "location": place.get("geometry", {}).get("location")
                    })

            except Exception as e:
                return {"error": str(e)}, 500

        return results, 200
