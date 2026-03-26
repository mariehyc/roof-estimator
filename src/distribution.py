import random

def generate_price_distribution(base_price, variance, neighborhood_mult, n=100):
    adjusted_base = base_price * neighborhood_mult
    samples = []

    for _ in range(n):
        factor = random.uniform(1 - variance, 1 + variance)
        samples.append(adjusted_base * factor)

    min_val = min(samples)
    max_val = max(samples)
    avg_val = sum(samples) / len(samples)
    spread = max_val - min_val

    return {
        "min": round(min_val, 0),
        "max": round(max_val, 0),
        "avg": round(avg_val, 0),
        "spread": round(spread, 0),
        "samples": samples
    }