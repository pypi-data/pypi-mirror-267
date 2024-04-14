import pandas as pd


def age_projection_per_model_point(model_points, output):
    duration_if = output["MP_ID"].map(
        model_points.set_index("MP_ID")["DURATIONIF_M"]
    )
    age_at_entry = output["MP_ID"].map(
        model_points.set_index("MP_ID")["AGE_AT_ENTRY"]
    )
    return (
        age_at_entry + ((duration_if + output["month_index"]) // 12)
    ).rename("Age")


def tech_assumptions_projection_output(
    model_points, output, tech_assumptions, product, col_name
):
    duration_if = output["MP_ID"].map(
        model_points.set_index("MP_ID")["DURATIONIF_M"]
    )
    projection_yr = (
        (((duration_if + output["month_index"]) // 12) + 1)
        .clip(upper=11)
        .rename("proj_yr")
    )

    model_points["tech_id"] = model_points["PRODUCT_ID"].map(
        product.set_index("PRODUCT_ID")["TECH_ASSUMPTION_ID"]
    )
    tech_ids_output = output["MP_ID"].map(
        model_points.set_index("MP_ID")["tech_id"]
    )
    t2 = pd.concat([tech_ids_output, projection_yr], axis=1)

    merged_df = pd.merge(
        t2,
        tech_assumptions,
        left_on=["MP_ID", "proj_yr"],
        right_on=["TECH_ASSUMPTION_ID", "PROJECTION_YR"],
        how="inner",
        validate="m:1",
    )

    return merged_df[col_name]


def adjusted_present_value(
    model_points, output, tech_assumptions, product, cashflow
):

    output_copy = output.copy()
    annual_int_rate = tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "INT_RATE"
    )
    monthly_int_rate = (1 + annual_int_rate) ** (1 / 12) - 1
    discount_factor = 1 / (1 + monthly_int_rate) ** (
        output_copy["month_index"] + 1
    )

    output_copy["produit"] = output_copy[cashflow] * discount_factor
    output_copy = output_copy.iloc[::-1]
    grouped_data = output_copy.groupby("MP_ID")
    output_copy["van"] = grouped_data["produit"].cumsum()
    output_copy = output_copy.iloc[::-1]

    return output_copy["van"] / discount_factor
