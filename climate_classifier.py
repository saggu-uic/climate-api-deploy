from flask import Flask, request, jsonify
import rasterio
from rasterio.sample import sample_gen
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# LCZ label to class name
LCZ_CLASSES = {
    1: "Compact high-rise",
    2: "Compact mid-rise",
    3: "Compact low-rise",
    4: "Open high-rise",
    5: "Open mid-rise",
    6: "Open low-rise",
    7: "Lightweight low-rise",
    8: "Large low-rise",
    9: "Sparsely built",
    10: "Heavy industry",
    11: "Dense trees",
    12: "Scattered trees",
    13: "Bush, scrub",
    14: "Low plants",
    15: "Bare rock or paved",
    16: "Bare soil or sand",
    17: "Water"
}

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
        lat = data["lat"]
        lon = data["lon"]

        # Load LCZ raster
        with rasterio.open("lcz_filter_v3.tif") as lcz_ds:
            lcz_sample = list(lcz_ds.sample([(lon, lat)]))[0][0]

        # Load Köppen raster
        with rasterio.open("koppen_geiger_0p00833333.tif") as koppen_ds:
            koppen_sample = list(koppen_ds.sample([(lon, lat)]))[0][0]

        # Convert to int for mapping
        lcz_label = int(lcz_sample)
        koppen_label = int(koppen_sample)

        return jsonify({
            "lcz_class": LCZ_CLASSES.get(lcz_label, "Unknown"),
            "koppen_class": KOPPEN_CLASSES.get(koppen_label, "Unknown")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

