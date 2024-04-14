from furtheredge.modules.universal_life import tools
from furtheredge.modules.universal_life.sub_modules.reserve import _sar_death1
import pandas as pd
import numpy as np


def prospective_calculation(model_points, output, tech_assumptions, product):
    # print("Prospective calculation")

    output["PREM_PROS"] = _prem_pros(output)
    output["COMISSION_AMT"] = commission_amt(
        model_points, output, tech_assumptions, product
    )
    output["DEATH_CLAIMS"] = death_claim(
        model_points, output, tech_assumptions, product
    )
    output["SURR_CLAIM"] = surrender_claims(
        model_points, output, tech_assumptions, product
    )

    output["MATURITY_CLAIM"] = maturity_claims(model_points, output)

    output["MAIN_EXPENS"] = maintenance_expenses(
        model_points, output, tech_assumptions, product
    )

    output["CEDED_SA"] = ceded_sum_assured(model_points, output)

    output["CESSION_RATE"] = cession_rate(model_points, output)

    output["PREM_REINS"] = premium_paid_to_reinsurer(
        model_points, output, tech_assumptions, product
    )
    output["COMISS_REINS"] = commission_received_from_reinsurer(
        model_points, output, tech_assumptions, product
    )
    output["CLAIM_REINS"] = claims_paid_by_reinsurer(
        model_points, output, tech_assumptions, product
    )
    output["REINS_PROF_SHAR"] = reinsurance_profit_sharing(output)

    output["APV_PREM"] = adjusted_present_value_premium(
        model_points, output, tech_assumptions, product
    )

    output["APV_DEATH"] = adjusted_present_value_death(
        model_points, output, tech_assumptions, product
    )

    output["APV_SURR"] = adjusted_present_value_surr(
        model_points, output, tech_assumptions, product
    )

    output["APV_MATURITY"] = adjusted_present_value_maturity(
        model_points, output, tech_assumptions, product
    )

    output["APV_EXPENSES"] = adjusted_present_value_expenses(
        model_points, output, tech_assumptions, product
    )


def _prem_pros(output):

    return output["PREM_DUR"] * output["TPX"]


def commission_amt(model_points, output, tech_assumptions, product):

    commissions_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COMMISSIONS_PC"
    )
    return output["PREM_PROS"] * commissions_pc


def death_claim(model_points, output, tech_assumptions, product):
    cover_1_survival_probability = (1 - output["MORTALITY_RATE_DEATH"]) ** (
        1 / 12
    )
    or_survival_probability = (1 - output["MORTALITY_RATE_OR"]) ** (1 / 12)
    cover_7_survival_probability = (1 - output["MORTALITY_RATE_ADB"]) ** (
        1 / 12
    )
    tpx = output["TPX"]
    if_ind = output["IND_IF"]
    sar_death1 = _sar_death1(model_points, output, tech_assumptions, product)
    prm_allocation_amount_av_fund = (
        output["AV_FUND_VALUE"] + output["PREM_ALL_AMT_RES"]
    )
    return (
        prm_allocation_amount_av_fund * (1 - cover_1_survival_probability)
        + prm_allocation_amount_av_fund * (1 - or_survival_probability)
    ) * tpx * if_ind + (
        sar_death1 * (1 - cover_1_survival_probability)
        + (1 - or_survival_probability) * (1 - cover_7_survival_probability)
    ) * tpx * if_ind


def surrender_claims(model_points, output, tech_assumptions, product):
    death_mortality_rate = output["MORTALITY_RATE_DEATH"]
    or_mortality_rate = output["MORTALITY_RATE_OR"]
    abd_mortality_rate = output["MORTALITY_RATE_ADB"]
    if_ind = output["IND_IF"]
    tpx = output["TPX"]

    surrender_charge = tools.tech_assumptions_projection_output(
        model_points,
        output,
        tech_assumptions,
        product,
        "SURRENDER_CHARGE_FIXED_AMT",
    )

    av_fund = output["AV_FUND_VALUE"]
    lapse_rate = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "LAPSE_RATE_PC"
    )
    unclaimed_policies = (1 - lapse_rate) ** (1 / 12)

    surr_claim = (
        av_fund
        * (1 - unclaimed_policies)
        * tpx
        * if_ind
        * (1 - surrender_charge)
        * (1 - death_mortality_rate - or_mortality_rate - abd_mortality_rate)
        ** (1 / 12)
    )
    return surr_claim


def maturity_claims(model_points, output):

    output_temp = output.copy()
    duration_if = output["MP_ID"].map(
        model_points.set_index("MP_ID")["DURATIONIF_M"]
    )
    projected_m = duration_if + output["month_index"]
    policy_term_m = output["MP_ID"].map(
        model_points.set_index("MP_ID")["POLICY_TERM_M"]
    )
    av_fund = output_temp["AV_FUND_VALUE"]

    conditional_value = pd.Series(0, index=output.index)
    conditional_value[projected_m == policy_term_m] = av_fund.astype(
        conditional_value.dtype
    )
    tpx = output["TPX"]
    maturity_claim = conditional_value * tpx
    return maturity_claim


def maintenance_expenses(model_points, output, tech_assumptions, product):
    tpx = output["TPX"]
    if_ind = output["IND_IF"]
    prem_pros = output["PREM_PROS"]
    fixed_loading_amt = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "FIXED_LOADING_AMT"
    )

    inflation_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "INFLATION_PC"
    )

    variable_loading_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "VARIABLE_LOADING_PC"
    )

    duration = 1
    main_expens = (
        tpx
        * fixed_loading_amt
        / 12
        * if_ind
        * (1 + inflation_pc) ** (duration - 1)
        + variable_loading_pc * prem_pros
    ) * if_ind
    return main_expens


def ceded_sum_assured(model_points, output):

    sa_cov1_amt = output["MP_ID"].map(
        model_points.set_index("MP_ID")["SA_COV1_AMT"]
    )
    ret_cov1_amt = output["MP_ID"].map(
        model_points.set_index("MP_ID")["RET_COV1_AMT"]
    )
    ceded_sa = np.maximum(sa_cov1_amt - ret_cov1_amt, 0)
    return ceded_sa


def cession_rate(model_points, output):
    ceded_sa = output["CEDED_SA"]
    sa_cov1_amt = output["MP_ID"].map(
        model_points.set_index("MP_ID")["SA_COV1_AMT"]
    )
    cess_rate = ceded_sa / sa_cov1_amt
    return cess_rate


def premium_paid_to_reinsurer(model_points, output, tech_assumptions, product):

    cess_rate = output["CESSION_RATE"]

    coi_death = output["COI_DEATH"]
    coi_or = output["COI_OTHER_RIDERS"]
    coi_adb = output["COI_ADB"]
    tpx = output["TPX"]
    coi = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "COI_PC"
    )
    prem_reins = cess_rate * (coi_death + coi_or + coi_adb) * tpx / coi

    return prem_reins


def commission_received_from_reinsurer(
    model_points, output, tech_assumptions, product
):

    ri_commission_pc = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "RI_COMMISSION_PC"
    )
    prem_reins = output["PREM_REINS"]
    projection_yr = (output["month_index"] // 12) + 1

    commission_year_1 = -ri_commission_pc * prem_reins
    condition_year_1 = projection_yr == 1
    comiss_reins = commission_year_1 * prem_reins * condition_year_1
    return comiss_reins


def claims_paid_by_reinsurer(model_points, output, tech_assumptions, product):
    cess_rate = output["CESSION_RATE"]
    sar_death1 = output["SAR_DEATH"]
    sar_or = output["SAR_OR"]
    sar_adb = output["SAR_ADB"]

    death_survival_proba = (1 - output["MORTALITY_RATE_DEATH"]) ** (1 / 12)
    or_survival_proba = (1 - output["MORTALITY_RATE_OR"]) ** (1 / 12)
    adb_survival_proba = (1 - output["MORTALITY_RATE_ADB"]) ** (1 / 12)

    tpx = output["TPX"]
    if_ind = output["IND_IF"]
    emf = tools.tech_assumptions_projection_output(
        model_points, output, tech_assumptions, product, "EMF"
    )
    claim_reins = (
        cess_rate
        * (
            sar_death1 * (1 - death_survival_proba)
            + sar_or * (1 - or_survival_proba)
            + sar_adb * (1 - adb_survival_proba)
        )
        * tpx
        * if_ind
    ) / emf
    return claim_reins


def reinsurance_profit_sharing(output):
    prem_reins = output["PREM_REINS"]
    comiss_reins = output["COMISS_REINS"]
    claim_reins = output["CLAIM_REINS"]
    reins_prof_shar = np.maximum(
        0.5 * (1 - 0.15) * (-prem_reins) * comiss_reins * claim_reins, 0
    )
    return reins_prof_shar


def adjusted_present_value_premium(
    model_points, output, tech_assumptions, product
):
    apv_prem = tools.adjusted_present_value(
        model_points, output, tech_assumptions, product, "PREM_PROS"
    )

    return apv_prem


def adjusted_present_value_death(
    model_points, output, tech_assumptions, product
):

    apv_death = tools.adjusted_present_value(
        model_points, output, tech_assumptions, product, "DEATH_CLAIMS"
    )

    return apv_death


def adjusted_present_value_surr(
    model_points, output, tech_assumptions, product
):
    apv_surr = tools.adjusted_present_value(
        model_points, output, tech_assumptions, product, "SURR_CLAIM"
    )

    return apv_surr


def adjusted_present_value_maturity(
    model_points, output, tech_assumptions, product
):
    apv_maturity = tools.adjusted_present_value(
        model_points, output, tech_assumptions, product, "MATURITY_CLAIM"
    )

    return apv_maturity


def adjusted_present_value_expenses(
    model_points, output, tech_assumptions, product
):
    apv_expenses = tools.adjusted_present_value(
        model_points, output, tech_assumptions, product, "PREM_REINS"
    )

    return apv_expenses
