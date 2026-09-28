import csv
import os
import matplotlib.pyplot as plt

# Read dataset
with open("data/house_prices.csv", "r") as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Convert values
area = [float(row["Area_sqft"]) for row in data]
bedrooms = [float(row["Bedrooms"]) for row in data]
house_age = [float(row["HouseAge"]) for row in data]
price = [float(row["Price"]) for row in data]

# Create graphs folder
os.makedirs("outputs/graphs", exist_ok=True)

# 1. Area vs Price
plt.figure()
plt.scatter(area, price)
plt.xlabel("Area (sqft)")
plt.ylabel("House Price")
plt.title("Area vs House Price")
plt.savefig("outputs/graphs/area_vs_price.png")
plt.close()

# 2. Bedrooms vs Price
plt.figure()
plt.scatter(bedrooms, price)
plt.xlabel("Number of Bedrooms")
plt.ylabel("House Price")
plt.title("Bedrooms vs House Price")
plt.savefig("outputs/graphs/bedrooms_vs_price.png")
plt.close()

# 3. House Age vs Price
plt.figure()
plt.scatter(house_age, price)
plt.xlabel("House Age")
plt.ylabel("House Price")
plt.title("House Age vs House Price")
plt.savefig("outputs/graphs/house_age_vs_price.png")
plt.close()

print("=" * 50)
print("GRAPHS CREATED SUCCESSFULLY")
print("=" * 50)

print("\nGraphs saved in:")
print("outputs/graphs/")