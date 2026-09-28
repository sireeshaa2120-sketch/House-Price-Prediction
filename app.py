from flask import Flask, render_template, request
import csv

app = Flask(__name__)


# Load training information
with open("data/house_prices.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)


# Calculate average price per square foot
total_area = sum(float(row["Area_sqft"]) for row in data)
total_price = sum(float(row["Price"]) for row in data)

price_per_sqft = total_price / total_area


def predict_price(
    location,
    property_type,
    area,
    bedrooms,
    bathrooms,
    year_built,
    parking,
    amenities
):
    # Base price
    price = area * price_per_sqft

    # Location adjustment
    location_adjustment = {
        "Vizag": 800000,
        "Vijayawada": 700000,
        "Hyderabad": 1500000,
        "Bangalore": 1800000,
        "Chennai": 1400000
    }

    price += location_adjustment.get(location, 0)

    # Property type adjustment
    property_adjustment = {
        "Apartment": 500000,
        "House": 900000,
        "Villa": 1800000
    }

    price += property_adjustment.get(property_type, 0)

    # Other features
    price += bedrooms * 200000
    price += bathrooms * 150000
    price += parking * 100000
    price += amenities * 75000

    # House age
    house_age = 2026 - year_built
    price -= house_age * 30000

    # Minimum price
    price = max(price, 1000000)

    return price


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        location = request.form["location"]
        property_type = request.form["property_type"]

        area = float(request.form["area"])
        bedrooms = int(request.form["bedrooms"])
        bathrooms = int(request.form["bathrooms"])
        year_built = int(request.form["year_built"])
        parking = int(request.form["parking"])
        amenities = int(request.form["amenities"])

        predicted_price = predict_price(
            location,
            property_type,
            area,
            bedrooms,
            bathrooms,
            year_built,
            parking,
            amenities
        )

        return render_template(
            "result.html",
            price=predicted_price
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)