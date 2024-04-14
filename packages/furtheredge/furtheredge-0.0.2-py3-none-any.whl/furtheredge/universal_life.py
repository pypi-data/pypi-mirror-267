import pandas as pd
from modules.universal_life.run import universal_life_module


def universal_life():
    model_points = pd.read_csv("furtheredge/inputs/model_points2.csv")
    ri_rates = pd.read_csv(
        "furtheredge/inputs/ri_rates.csv", sep=";", decimal=","
    )
    wop_rates = pd.read_csv(
        "furtheredge/inputs/wop_rates.csv", sep=";", decimal=","
    )
    tech_assumptions = pd.read_csv(
        "furtheredge/inputs/tech_assumptions.csv", sep=";", decimal=","
    )
    product = pd.read_csv(
        "furtheredge/inputs/product.csv", sep=";", decimal=","
    )

    # print(f"Model points length: {len(model_points)}")

    result_universal_life = universal_life_module(
        model_points,
        {"time_horizon": 50, "projection_date": "2023-10-31"},
        tech_assumptions,
        ri_rates,
        wop_rates,
        product,
    )

    # print(result_universal_life[result_universal_life["MP_ID"] == 169])
    return result_universal_life
