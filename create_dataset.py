import pandas as pd
import numpy as np
import os

# Make the results reproducible
np.random.seed(42)

# Number of houses
number_of_houses = 1000

# Create basic house features
data = {
    "Location": np.random.choice(
        ["Vizag", "Vijayawada", "Hyderabad", "Bangalore", "Chennai"],
        number_of_houses
    ),

    "PropertyType": np.random.choice(
        ["Apartment", "House", "Villa"],
        number_of_houses
    ),

    "Area_sqft": np.random.randint(
        600, 3501, number_of_houses
    ),

    "Bedrooms": np.random.randint(
        1, 6, number_of_houses
    ),

    "Bathrooms": np.random.randint(
        1, 5, number_of_houses
    ),

    "YearBuilt": np.random.randint(
        1990, 2026, number_of_houses
    ),

    "Parking": np.random.randint(
        0, 3, number_of_houses
    ),

    "Amenities": np.random.randint(
        0, 6, number_of_houses
    )
}

# Convert dictionary into DataFrame
df = pd.DataFrame(data)

# Location price contribution
location_price = {
    "Vizag": 800000,
    "Vijayawada": 700000,
    "Hyderabad": 1500000,
    "Bangalore": 1800000,
    "Chennai": 1400000
}

df["LocationPrice"] = df["Location"].map(location_price)

# Property type contribution
property_price = {
    "Apartment": 500000,
    "House": 900000,
    "Villa": 1800000
}

df["PropertyTypePrice"] = df["PropertyType"].map(property_price)

# Calculate age of house
df["HouseAge"] = 2026 - df["YearBuilt"]

# Generate house price
df["Price"] = (
    (df["Area_sqft"] * 4500)
    + (df["Bedrooms"] * 200000)
    + (df["Bathrooms"] * 150000)
    + (df["Parking"] * 100000)
    + (df["Amenities"] * 75000)
    + df["LocationPrice"]
    + df["PropertyTypePrice"]
    - (df["HouseAge"] * 30000)
)

# Add a small amount of random variation
noise = np.random.normal(0, 300000, number_of_houses)

df["Price"] = df["Price"] + noise

# Make sure prices are positive
df["Price"] = df["Price"].clip(lower=1000000)

# Remove helper columns from final dataset
df = df.drop(
    columns=["LocationPrice", "PropertyTypePrice"]
)

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Save dataset
file_path = "data/house_prices.csv"
df.to_csv(file_path, index=False)

print("=" * 50)
print("HOUSE PRICE DATASET CREATED SUCCESSFULLY")
print("=" * 50)

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 records:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nDataset saved to:")
print(file_path)