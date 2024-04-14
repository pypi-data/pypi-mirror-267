import pandas as pd
import numpy as np
from furtheredge.modules.universal_life import tools

payment_months = {
    1: [12],
    2: [6, 12],
    4: [3, 6, 9, 12],
    12: list(range(1, 13)),
}


def duration_calculation(
    model_points, output, tech_assumptions, ri_rates, wop_rates, product
):
    # print("Duration calculation")

    output["IND_PAY"] = _payment_month(model_points, output)
    output["IND_IF"] = _indicator_policy_if(model_points, output)
    output["PREM_DUR"] = _premium_duration(model_points, output)
    output["FEE_AMT"] = _fees_amount(
        model_points, output, tech_assumptions, product
    )
    output["ACQ_LOAD"] = _acquisition_loading(
        model_points, output, tech_assumptions, product
    )
    output["PREM_ALL_AMT_DUR"] = _premium_allocation_amount_dur(output)
    output["QX_DEATH"] = _qx_death(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["QX_PTD"] = _qx_ptd(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["QX_PTD_ADDITIONAL"] = _qx_ptd_additional(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["QX_CRITICAL_ILLNESS_ADD"] = _qx_critical_illness_additional(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["QX_PPD"] = _qx_ppd(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["QX_ADB"] = _qx_adb(
        model_points, output, ri_rates, tech_assumptions, product
    )
    output["QX_WOP"] = _qx_wop(
        model_points, output, wop_rates, tech_assumptions, product
    )
    output["QX_CRITICAL_ILLNESS_ACC"] = _qx_critical_illness_accelerated(
        model_points, output, ri_rates, tech_assumptions, product
    )
    return output


def _payment_month(model_points, output):
    mp_pay_mode_dict = dict(
        zip(model_points["MP_ID"], model_points["PAY_MODE"])
    )

    def payment_indicator(row):
        month = row["fin_mois"].month
        mp_id = row["MP_ID"]
        current_pay_mode = mp_pay_mode_dict.get(mp_id)

        if month in payment_months.get(current_pay_mode, []):
            return 1
        else:
            return 0

    return output.apply(payment_indicator, axis=1)


def _indicator_policy_if(model_points, output):

    policy_term_m = output["MP_ID"].map(
        model_points.set_index("MP_ID")["POLICY_TERM_M"]
    )
    duration_if_m = output["MP_ID"].map(
        model_points.set_index("MP_ID")["DURATIONIF_M"]
    )

    return (output["month_index"] <= (policy_term_m - duration_if_m)).astype(
        np.int64
    )


def _premium_duration(model_points, output, persistency_rate=1):

    modal_prem = output["MP_ID"].map(
        model_points.set_index("MP_ID")["MODAL_PREM_AMT"]
    )

    return modal_prem * output["IND_PAY"] * output["IND_IF"] * persistency_rate


def _fees_amount(model_points, output, tech_assumptions, product):

    sa_death = output["MP_ID"].map(
        model_points.set_index("MP_ID")["SA_COV1_AMT"]
    )

    sa_loading_pm = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "SA_LOADING_PM"
    )

    return sa_death * output["IND_IF"] * ((sa_loading_pm / 1000) / 12)


def _acquisition_loading(model_points, output, tech_assumptions, product):

    modal_prem = output["MP_ID"].map(
        model_points.set_index("MP_ID")["MODAL_PREM_AMT"]
    )

    prem_loading_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "PREM_LOADING_PC"
    )

    return modal_prem * prem_loading_pc * output["IND_PAY"]


def _premium_allocation_amount_dur(output):
    return output["PREM_DUR"] - output["FEE_AMT"] - output["ACQ_LOAD"]


def _qx_death(model_points, output, ri_rates, tech_assumptions, product):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_death_rate = (
        (ri_rates.loc[ri_rates["COVER"] == "Death", :])
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    x_prem_cov1_pc = output["MP_ID"].map(
        model_points.set_index("MP_ID")["X_PREM_COV11_PC"]
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    return (
        coi_pc
        * ((cover_death_rate / 1000) / 12)
        * output["IND_IF"]
        * (1 + x_prem_cov1_pc)
    )


def _qx_ptd(model_points, output, ri_rates, tech_assumptions, product):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_tpd_rate = (
        (
            (
                ri_rates.loc[ri_rates["COVER"] == "TPD Accelerator Any", :]
            ).reset_index(drop=True)
        )
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov2_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV2_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return (
        coi_pc * ((cover_tpd_rate / 1000) / 12) * output["IND_IF"] * sa_cov2_pc
    )


def _qx_ptd_additional(
    model_points, output, ri_rates, tech_assumptions, product
):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_tpd_add_rate = (
        (
            (
                ri_rates.loc[ri_rates["COVER"] == "TPD Accelerator Any", :]
            ).reset_index(drop=True)
        )
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov3_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV3_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return (
        coi_pc
        * ((cover_tpd_add_rate / 1000) / 12)
        * output["IND_IF"]
        * sa_cov3_pc
    )


def _qx_critical_illness_additional(
    model_points, output, ri_rates, tech_assumptions, product
):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_critical_illness_add_rate = (
        (
            (
                ri_rates.loc[ri_rates["COVER"] == "CI Accelerator (Male)", :]
            ).reset_index(drop=True)
        )
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov4_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV4_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return (
        coi_pc
        * ((cover_critical_illness_add_rate / 1000) / 12)
        * output["IND_IF"]
        * sa_cov4_pc
    )


def _qx_ppd(model_points, output, ri_rates, tech_assumptions, product):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_ppd_rate = (
        (
            (
                ri_rates.loc[ri_rates["COVER"] == "Accidental PPD", :]
            ).reset_index(drop=True)
        )
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov6_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV6_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return (
        coi_pc * ((cover_ppd_rate / 1000) / 12) * output["IND_IF"] * sa_cov6_pc
    )


def _qx_adb(model_points, output, ri_rates, tech_assumptions, product):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_adb_rate = (
        (
            (
                ri_rates.loc[ri_rates["COVER"] == "Accidental Death", :]
            ).reset_index(drop=True)
        )
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov7_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV7_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return (
        coi_pc * ((cover_adb_rate / 1000) / 12) * output["IND_IF"] * sa_cov7_pc
    )


def _qx_wop(model_points, output, wop_rates, tech_assumptions, product):

    age = tools.age_projection_per_model_point(model_points, output)

    projection_yr = (output["month_index"] // 12) + 1

    t1 = pd.concat([age, projection_yr], axis=1)
    merged_df = pd.merge(
        t1,
        wop_rates,
        left_on=["Age", "month_index"],
        right_on=["AGE", "PROJ_YR"],
        how="inner",
        validate="m:1",
    )
    wop_rate = merged_df["RATE"]

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov8_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV8_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return coi_pc * ((wop_rate / 1000) / 12) * output["IND_IF"] * sa_cov8_pc


def _qx_critical_illness_accelerated(
    model_points, output, ri_rates, tech_assumptions, product
):

    age = tools.age_projection_per_model_point(model_points, output)

    cover_critical_illness_acc_rate = (
        (
            (
                ri_rates.loc[ri_rates["COVER"] == "CI Accelerator (Male)", :]
            ).reset_index(drop=True)
        )
        .loc[age, "RATE"]
        .reset_index(drop=True)
    )

    coi_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )

    sa_cov10_pc = (
        output["MP_ID"]
        .map(model_points.set_index("MP_ID")["SA_COV10_AMT"])
        .map(lambda x: 1 if x != 0 else 0)
    )

    return (
        coi_pc
        * ((cover_critical_illness_acc_rate / 1000) / 12)
        * output["IND_IF"]
        * sa_cov10_pc
    )
