import pandas as pd
from furtheredge.modules.universal_life.run import universal_life_module
import pkg_resources


def universal_life():
    package_dir = pkg_resources.resource_filename("furtheredge", "")

    model_points_path = package_dir + "/inputs/model_points2.csv"
    ri_rates_path = package_dir + "/inputs/ri_rates.csv"
    wop_rates_path = package_dir + "/inputs/wop_rates.csv"
    tech_assumptions_path = package_dir + "/inputs/tech_assumptions.csv"
    product_path = package_dir + "/inputs/product.csv"

    model_points = pd.read_csv(model_points_path)
    ri_rates = pd.read_csv(ri_rates_path, sep=";", decimal=",")
    wop_rates = pd.read_csv(wop_rates_path, sep=";", decimal=",")
    tech_assumptions = pd.read_csv(tech_assumptions_path, sep=";", decimal=",")
    product = pd.read_csv(product_path, sep=";", decimal=",")

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


# result_universal_life = universal_life()
# result_universal_life.to_csv(
#     "furtheredge/outputs/universal_life_output.csv", index=False
# )
