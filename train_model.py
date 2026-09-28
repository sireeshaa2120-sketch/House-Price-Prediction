import csv
import math
import os
import random

# Load dataset
with open("data/house_prices.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Convert important columns to numbers
for row in data:
    row["Area_sqft"] = float(row["Area_sqft"])
    row["Bedrooms"] = float(row["Bedrooms"])
    row["Bathrooms"] = float(row["Bathrooms"])
    row["YearBuilt"] = float(row["YearBuilt"])
    row["Parking"] = float(row["Parking"])
    row["Amenities"] = float(row["Amenities"])
    row["HouseAge"] = float(row["HouseAge"])
    row["Price"] = float(row["Price"])

# Shuffle data
random.seed(42)
random.shuffle(data)

# 80% training, 20% testing
split = int(len(data) * 0.8)

train_data = data[:split]
test_data = data[split:]

# Calculate average price per square foot from training data
total_area = sum(row["Area_sqft"] for row in train_data)
total_price = sum(row["Price"] for row in train_data)

price_per_sqft = total_price / total_area

# Prediction function
def predict_price(row):
    price = row["Area_sqft"] * price_per_sqft

    price += row["Bedrooms"] * 200000
    price += row["Bathrooms"] * 150000
    price += row["Parking"] * 100000
    price += row["Amenities"] * 75000

    # Location adjustment
    location_adjustment = {
        "Vizag": 800000,
        "Vijayawada": 700000,
        "Hyderabad": 1500000,
        "Bangalore": 1800000,
        "Chennai": 1400000
    }

    price += location_adjustment.get(row["Location"], 0)

    # Property type adjustment
    property_adjustment = {
        "Apartment": 500000,
        "House": 900000,
        "Villa": 1800000
    }

    price += property_adjustment.get(row["PropertyType"], 0)

    price -= row["HouseAge"] * 30000

    return max(price, 1000000)


# Make predictions
actual = []
predicted = []

for row in test_data:
    actual_price = row["Price"]
    predicted_price = predict_price(row)

    actual.append(actual_price)
    predicted.append(predicted_price)


# Calculate MSE
mse = sum(
    (actual[i] - predicted[i]) ** 2
    for i in range(len(actual))
) / len(actual)

# Calculate RMSE
rmse = math.sqrt(mse)

# Calculate R-squared
mean_actual = sum(actual) / len(actual)

ss_total = sum(
    (value - mean_actual) ** 2
    for value in actual
)

ss_residual = sum(
    (actual[i] - predicted[i]) ** 2
    for i in range(len(actual))
)

r2 = 1 - (ss_residual / ss_total)


# Create folders
os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# Save model information
with open("models/house_price_model.txt", "w") as file:
    file.write("House Price Prediction Model\n")
    file.write("============================\n")
    file.write(f"Price per square foot: {price_per_sqft}\n")
    file.write("Model type: Regression-based price prediction\n")


# Save metrics
with open("outputs/metrics.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Metric", "Value"])
    writer.writerow(["MSE", mse])
    writer.writerow(["RMSE", rmse])
    writer.writerow(["R2 Score", r2])


# Display results
print("=" * 50)
print("HOUSE PRICE MODEL TRAINED SUCCESSFULLY")
print("=" * 50)

print(f"\nTraining records: {len(train_data)}")
print(f"Testing records: {len(test_data)}")

print(f"\nMean Squared Error: {mse:.2f}")
print(f"Root Mean Squared Error: {rmse:.2f}")
print(f"R-squared Score: {r2:.4f}")

print("\nModel saved to:")
print("models/house_price_model.txt")

print("\nMetrics saved to:")
print("outputs/metrics.csv")