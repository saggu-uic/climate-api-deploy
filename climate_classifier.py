from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim
import rasterio
import traceback

app = Flask(__name__)
CORS(app)

# Köppen label to class name
KOPPEN_CLASSES = {
    1: "Af",   2: "Am",   3: "Aw/As",
    4: "BWh",  5: "BWk",  6: "BSh",  7: "BSk",
    8: "Csa",  9: "Csb", 10: "Csc",
   11: "Cwa", 12: "Cwb", 13: "Cwc",
   14: "Cfa", 15: "Cfb", 16: "Cfc",
   17: "Dsa", 18: "Dsb", 19: "Dsc", 20: "Dsd",
   21: "Dwa", 22: "Dwb", 23: "Dwc", 24: "Dwd",
   25: "Dfa", 26: "Dfb", 27: "Dfc", 28: "Dfd",
   29: "ET",  30: "EF"
}

@app.route("/classify", methods=["POST"])
def classify():
    try:
        data = request.json
        print("Received data:", data, flush=True)

        address = data.get("address")
        if not address:
            return jsonify({"error": "Address is required"}), 400

        # Geocode the address
        geolocator = Nominatim(user_agent="climate_classifier")
        location = geolocator.geocode(address)
        if not location:
            return jsonify({"error": "Address not found"}), 400

        lat, lon = location.latitude, location.longitude
        print(f"Geocoded address to lat: {lat}, lon: {lon}", flush=True)

        # Read the raster and classify
        raster_path = "koppen_geiger_0p00833333.tif"
        print(f"Opening raster file: {raster_path}", flush=True)

        with rasterio.open(raster_path) as koppen_ds:
            koppen_sample = list(koppen_ds.sample([(lon, lat)]))[0][0]
            koppen_label = int(koppen_sample)

        koppen_class = KOPPEN_CLASSES.get(koppen_label, "Unknown")
        print(f"Köppen label: {koppen_label}, classified as: {koppen_class}", flush=True)

        return jsonify({
            "lat": lat,
            "lon": lon,
            "koppen_class": koppen_class
        })

    except Exception as e:
        print("Exception occurred:", flush=True)
        traceback.print_exc()  # This shows full traceback in logs
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
