import json

def load_json(path):
    with open(path) as f:
        return json.load(f)

def estimate_cost(input_data):
    config = load_json("config/pricing_config.json")
    city_data = load_json(f"data/{input_data['city'].lower()}.json")

    # convert sq ft → squares
    squares = input_data["area_sqft"] / 100

    # base costs
    material_cost = config["material_cost_per_sq"][input_data["material"]] * squares
    labor_cost = config["labor_cost_per_sq"] * squares

    base_cost = material_cost + labor_cost

    # multipliers
    pitch_mult = config["pitch_multiplier"][input_data["pitch"]]
    waste_mult = config["waste_factor"]
    city_mult = city_data["labor_index"]
    neighborhood_mult = city_data["neighborhoods"][input_data["neighborhood"]]

    adjusted = base_cost * pitch_mult * waste_mult * city_mult * neighborhood_mult

    # tear off
    if input_data.get("tear_off"):
        adjusted += config["tear_off_cost_per_sq"] * squares

    # variability
    variance = city_data["price_variance"]
    low = adjusted * (1 - variance)
    high = adjusted * (1 + variance)

    # uncertainty (hidden issues)
    high *= (1 + config["decking_uncertainty"])

    return {
        "base": round(adjusted, 0),
        "low": round(low, 0),
        "high": round(high, 0)
    }