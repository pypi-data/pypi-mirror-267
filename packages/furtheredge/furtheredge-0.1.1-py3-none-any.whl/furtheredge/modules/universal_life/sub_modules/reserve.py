from furtheredge.modules.universal_life import tools
import numpy as np
import pandas as pd


def reserve_calculation(model_points, output, tech_assumptions, product):
    # print("Reserve calculation")

    output["PREM_ALL_AMT_RES"] = _premium_allocation_amount_res(output)

    output["SAR_DEATH1"] = _sar_death1(
        model_points, output, tech_assumptions, product
    )

    output["SAR_DEATH2"] = _sar_death2(model_points, output)

    output["SAR_DEATH"] = _sar_death(model_points, output)

    output["SAR_OR"] = _sar_death(model_points, output)

    output["SAR_ADB2"] = _sar_adb2(model_points, output)

    output["SAR_ADB"] = _sar_adb(model_points, output)

    output["COI_DEATH"] = _coi_death(output)

    output["COI_OTHER_RIDERS"] = _coi_other_riders(output)

    output["COI_ADB"] = _coi_adb(output)

    output["FUND_VALUE"] = _fund_value(model_points, output)

    output["FMF"] = _fixed_management_fees(
        model_points, output, tech_assumptions, product
    )
    output["AV_FUND_VALUE"] = _av_fund_value(
        model_points, output, tech_assumptions, product
    )
    output["INTEREST"] = _interest(output)


def _premium_allocation_amount_res(output):
    return output["PREM_ALL_AMT_DUR"]


def _sar_death1(model_points, output_df, tech_assumptions, product):
    output = output_df.copy()
    annual_int_rate = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "INT_RATE"
    )
    monthly_int_rate = (1 + annual_int_rate) ** (1 / 12) - 1
    discount_factor = 1 / (1 + monthly_int_rate) ** (output["month_index"] + 1)

    output["produit"] = output["PREM_ALL_AMT_RES"] * discount_factor
    output = output.iloc[::-1]
    grouped_data = output.groupby("MP_ID")
    output["van"] = grouped_data["produit"].cumsum()
    output = output.iloc[::-1]
    output_temp = pd.DataFrame()
    output_temp["shifted_col"] = (
        output.groupby(["MP_ID"])["van"].shift(-1).fillna(0)
    )
    result = output_temp["shifted_col"] / discount_factor

    return result


def _sar_death2(model_points, output_df):
    output = output_df.copy()

    sa_cov1_amt = output["MP_ID"].map(
        model_points.set_index("MP_ID")["SA_COV1_AMT"]
    )
    cash_value_fund1 = output["MP_ID"].map(
        model_points.set_index("MP_ID")["CASH_VAL_FUND1"]
    )
    output["sar_death2"] = (
        sa_cov1_amt - cash_value_fund1 - output["PREM_ALL_AMT_RES"]
    )
    output.loc[output["sar_death2"] < 0, "sar_death2"] = 0
    return output["sar_death2"] * output["IND_IF"]


def _sar_death(model_points, output_df):
    output = output_df.copy()

    output["code_plan"] = output["MP_ID"].map(
        model_points.set_index("MP_ID")["PRODUCT_TYPE"]
    )

    return np.where(
        output["code_plan"] == "Education",
        output["SAR_DEATH1"],
        output["SAR_DEATH2"],
    )


def _sar_adb2(model_points, output_df):
    output = output_df.copy()

    sa_cov7_amt = output["MP_ID"].map(
        model_points.set_index("MP_ID")["SA_COV7_AMT"]
    )
    cash_value_fund1 = output["MP_ID"].map(
        model_points.set_index("MP_ID")["CASH_VAL_FUND1"]
    )
    output["sar_adb2"] = (
        sa_cov7_amt - cash_value_fund1 - output["PREM_ALL_AMT_RES"]
    )
    output.loc[output["sar_adb2"] < 0, "sar_adb2"] = 0
    return output["sar_adb2"] * output["IND_IF"]


def _sar_adb(model_points, output_df):

    output = output_df.copy()
    output["product_id"] = output["MP_ID"].map(
        model_points.set_index("MP_ID")["PRODUCT_ID"]
    )

    sar_death_affected_values = [1, 2, 3]

    output.loc[
        output["product_id"].isin(sar_death_affected_values), "sar_adb"
    ] = output["SAR_DEATH1"]

    adb2_affected_values = [4, 5, 6, 7]

    output.loc[output["product_id"].isin(adb2_affected_values), "sar_adb"] = (
        output["SAR_ADB2"]
    )

    return output["sar_adb"]


def _coi_death(output):
    return output["SAR_DEATH"] * output["QX_DEATH"]


def _coi_other_riders(output):
    return output["SAR_DEATH"] * (
        output["QX_PTD"]
        + output["QX_PTD_ADDITIONAL"]
        + output["QX_CRITICAL_ILLNESS_ADD"]
        + output["QX_PPD"]
        + output["QX_WOP"]
        + output["QX_CRITICAL_ILLNESS_ACC"]
    )


def _coi_adb(output):
    return output["SAR_DEATH"] * output["QX_ADB"]


def _fund_value(model_points, output):
    output_df = output.copy()
    merged_df = output_df.merge(
        model_points[["MP_ID", "CASH_VAL_FUND1"]], on="MP_ID", how="inner"
    )

    def calculate_fund_value(group):
        fund_values = []
        prev_fund_value = 0
        for index, row in group.iterrows():
            if row["month_index"] == 0:
                fund_value = (
                    row["PREM_ALL_AMT_RES"]
                    - row["COI_DEATH"]
                    - row["COI_OTHER_RIDERS"]
                    + row["CASH_VAL_FUND1"]
                ) * row["IND_IF"]
            else:
                fund_value = (
                    row["PREM_ALL_AMT_RES"]
                    - row["COI_DEATH"]
                    - row["COI_OTHER_RIDERS"]
                    + prev_fund_value
                ) * row["IND_IF"]
            fund_values.append(fund_value)
            prev_fund_value = fund_value
        group["FUND_VALUE"] = fund_values
        return group

    output_result = (
        merged_df.groupby("MP_ID")
        .apply(calculate_fund_value, include_groups=False)
        .reset_index(drop=True)
    )
    return output_result["FUND_VALUE"]


def _fixed_management_fees(model_points, output, tech_assumptions, product):
    fmf_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "FMF_PC"
    )
    return (fmf_pc * output["FUND_VALUE"]) / 12


def _av_fund_value(model_points, output, tech_assumptions, product):
    mgr_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "MGR_PC"
    )
    return (output["FUND_VALUE"] - output["FMF"]) * ((1 + mgr_pc) ** (1 / 12))


def _interest(output):
    return output["AV_FUND_VALUE"] - output["FUND_VALUE"]
