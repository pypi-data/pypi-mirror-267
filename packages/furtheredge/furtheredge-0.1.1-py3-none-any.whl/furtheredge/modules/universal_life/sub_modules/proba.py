from furtheredge.modules.universal_life import tools


def proba_calculation(
    model_points, output, tech_assumptions, ri_rates, product
):
    # print("Proba calculation")

    output["MORTALITY_RATE_DEATH"] = _mortality_rate_death(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["MORTALITY_RATE_OR"] = _mortality_rate_or(output)
    output["MORTALITY_RATE_ADB"] = _mortality_rate_adb(
        model_points, output, ri_rates
    )
    output["TPX"] = tpx(model_points, output, tech_assumptions, product)


def _mortality_rate_death(
    model_points, output, ri_rates, tech_assumptions, product
):
    emf = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "EMF"
    )

    age = tools.age_projection_per_model_point(model_points, output)
    cover_death_rate = (
        (ri_rates.loc[ri_rates["COVER"] == "Death", :])
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    x_prem_cov1_pc = output["MP_ID"].map(
        model_points.set_index("MP_ID")["X_PREM_COV11_PC"]
    )

    return (
        emf
        * (cover_death_rate / 1000)
        * output["IND_IF"]
        * (1 + x_prem_cov1_pc)
    )


def _mortality_rate_or(output):
    return (
        output["QX_PTD"]
        + output["QX_PTD_ADDITIONAL"]
        + output["QX_CRITICAL_ILLNESS_ADD"]
        + output["QX_PPD"]
        + output["QX_WOP"]
        + output["QX_CRITICAL_ILLNESS_ACC"]
    ) * 12


def _mortality_rate_adb(model_points, output, ri_rates):

    age = tools.age_projection_per_model_point(model_points, output)
    cover_adb_rate = (
        (ri_rates.loc[ri_rates["COVER"] == "CI Accelerator (Female)", :])
        .reset_index(drop=True)
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    return (cover_adb_rate / 1000) * output["IND_IF"]


def tpx(model_points, output, tech_assumptions, product):
    output_df = output.copy()
    death_survival_probability = (1 - output["MORTALITY_RATE_DEATH"]) ** (
        1 / 12
    )
    or_survival_probability = (1 - output["MORTALITY_RATE_OR"]) ** (1 / 12)
    adb_survival_probability = (1 - output["MORTALITY_RATE_ADB"]) ** (1 / 12)
    lapse_rate = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "LAPSE_RATE_PC"
    )
    unclaimed_policies = (1 - lapse_rate) ** (1 / 12)
    output_df["SURVIVAL_PROBABILITY"] = (
        death_survival_probability
        * or_survival_probability
        * adb_survival_probability
        * unclaimed_policies
    )

    def calculate_tpx_value(group):
        tpx_values = []
        prev_tpx_value = 0
        for index, row in group.iterrows():
            if row["month_index"] == 0:
                tpx_value = 1
            else:
                tpx_value = prev_tpx_value * row["SURVIVAL_PROBABILITY"]
            tpx_values.append(tpx_value)
            prev_tpx_value = tpx_value
        group["TPX"] = tpx_values
        return group

    output_result = (
        output_df.groupby("MP_ID")
        .apply(calculate_tpx_value, include_groups=False)
        .reset_index(drop=True)
    )
    return output_result["TPX"]
