import pandas as pd

from furtheredge.modules.universal_life.sub_modules.duration import (
    duration_calculation,
)
from furtheredge.modules.universal_life.sub_modules.reserve import (
    reserve_calculation,
)
from furtheredge.modules.universal_life.sub_modules.proba import (
    proba_calculation,
)
from furtheredge.modules.universal_life.sub_modules.prospective import (
    prospective_calculation,
)


def initialize_output_dataframe(
    number_of_model_points, duration_month, starting_projection_date
):
    dfs = []
    fin_mois = pd.date_range(
        start=starting_projection_date, periods=duration_month, freq="ME"
    )

    for i in range(1, number_of_model_points + 1):
        df = pd.DataFrame(
            {
                "MP_ID": i,
                "month_index": range(duration_month),
                "fin_mois": fin_mois,
            }
        )
        dfs.append(df)
    result_df = pd.concat(dfs, ignore_index=True)
    return result_df[["MP_ID", "month_index", "fin_mois"]]


# run_settings: { projection_date: DATE-STRING, time_horizon: int, simulation_number: int, scenario_id: string }
def universal_life_module(
    model_points, run_settings, tech_assumptions, ri_rates, wop_rates, product
):
    # print("Universal life module")
    output = initialize_output_dataframe(
        len(model_points),
        run_settings["time_horizon"],
        run_settings["projection_date"],
    )
    duration_calculation(
        model_points, output, tech_assumptions, ri_rates, wop_rates, product
    )
    reserve_calculation(model_points, output, tech_assumptions, product)
    proba_calculation(
        model_points, output, tech_assumptions, ri_rates, product
    )

    prospective_calculation(model_points, output, tech_assumptions, product)

    return output
