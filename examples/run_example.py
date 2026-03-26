from src.estimator import estimate_cost
from src.distribution import generate_price_distribution
from src.buckets import get_area_bucket

import matplotlib.pyplot as plt
import json


def plot_distribution(distribution):
    samples = distribution["samples"]

    plt.hist(samples, bins=15)
    plt.xlabel("Roof Cost ($)")
    plt.ylabel("Frequency")
    plt.title("Roof Price Distribution")

    # average line
    avg = distribution["avg"]
    plt.axvline(avg, linestyle='--', label="Average")

    # min / max
    plt.axvline(distribution["min"], linestyle=':', label="Min")
    plt.axvline(distribution["max"], linestyle=':', label="Max")

    # percentiles
    samples_sorted = sorted(samples)
    p10 = samples_sorted[int(0.1 * len(samples))]
    p90 = samples_sorted[int(0.9 * len(samples))]

    plt.axvline(p10, linestyle='-.', label="10th percentile")
    plt.axvline(p90, linestyle='-.', label="90th percentile")

    plt.legend()
    plt.show()


# ---------------------------
# INPUT
# ---------------------------

input_data = {
    "area_sqft": 2000,   # 20 squares
    "material": "asphalt",
    "pitch": "medium",
    "city": "Austin",
    "neighborhood": "suburban",
    "tear_off": True
}


# ---------------------------
# LOAD CITY DATA
# ---------------------------

with open("data/austin.json") as f:
    city_data = json.load(f)

neighborhood_mult = city_data["neighborhoods"][input_data["neighborhood"]]


# ---------------------------
# RUN ESTIMATE
# ---------------------------

estimate = estimate_cost(input_data)

distribution = generate_price_distribution(
    base_price=estimate["base"],
    variance=city_data["price_variance"],
    neighborhood_mult=neighborhood_mult
)

bucket = get_area_bucket(input_data["area_sqft"])


# ---------------------------
# OUTPUT
# ---------------------------

print("\n=== ESTIMATE ===")
print(estimate)

print("\n=== DISTRIBUTION ===")
print({
    "min": distribution["min"],
    "max": distribution["max"],
    "avg": distribution["avg"],
    "spread": distribution["spread"]
})

print("\n=== BUCKET ===")
print(bucket)


# ---------------------------
# VISUALIZATION
# ---------------------------

plot_distribution(distribution)