"""
PMC9087297 Preset Module

Paper: Cost-effectiveness of injectable cabotegravir (CAB-LA) PrEP vs oral PrEP
Setting: United States, MSM/TGW population
DOI: PMC9087297

This module provides 4 scenarios from the paper:
- VHR (very high risk) cohort with/without PrEP
- HR (high risk) cohort with/without PrEP
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from param_schema import create_default_params, CONSTANTS


# Paper metadata
PAPER_METADATA = {
    'pmcid': 'PMC9087297',
    'title': 'Cost-effectiveness of injectable cabotegravir (CAB-LA) PrEP vs oral PrEP',
    'setting': 'United States',
    'population': 'MSM/TGW',
    'currency_year': 2020,
    'time_horizon_years': 10,
    'discount_rate': 0.03,
}

# Extracted parameters from the paper
PAPER_PARAMS = {
    'population': {
        'mean_age_years': 30.1,
        'mean_age_months': 361,
        'gender_male_pct': 1.0,
    },
    'hiv_epidemiology': {
        'VHR': {
            'annual_incidence_per_100py': 5.32,
            'monthly_incidence': 0.00443,  # 5.32/100/12
            'cd4_at_infection': 667,
        },
        'HR': {
            'annual_incidence_per_100py': 1.54,
            'monthly_incidence': 0.00128,  # 1.54/100/12
            'cd4_at_infection': 667,
        },
    },
    'treatment': {
        'art_efficacy': 0.93,
        'art_adherence_ge90_pct': 0.71,
        'qol_on_art_range': (0.83, 0.87),
    },
    'costs_2020_usd': {
        'generic_ftdf_annual': 790,
        'generic_ftdf_monthly': 66,
        'branded_ftaf_annual': 17230,
        'branded_ftaf_monthly': 1436,
        'art_min_annual': 31560,
        'art_min_monthly': 2630,
        'art_max_annual': 68680,
        'art_max_monthly': 5723,
        'routine_hiv_care_min_annual': 3280,
        'routine_hiv_care_min_monthly': 273,
        'routine_hiv_care_max_annual': 32580,
        'routine_hiv_care_max_monthly': 2715,
    },
}

# Scenario definitions
PMC9087297_SCENARIOS = {
    'PMC9087297_VHR_NoPrEP': {
        'description': 'Very high risk cohort, no PrEP intervention',
        'risk_level': 'VHR',
        'enable_prep': False,
    },
    'PMC9087297_VHR_GenericPrEP': {
        'description': 'Very high risk cohort, generic F/TDF PrEP',
        'risk_level': 'VHR',
        'enable_prep': True,
    },
    'PMC9087297_HR_NoPrEP': {
        'description': 'High risk cohort, no PrEP intervention',
        'risk_level': 'HR',
        'enable_prep': False,
    },
    'PMC9087297_HR_GenericPrEP': {
        'description': 'High risk cohort, generic F/TDF PrEP',
        'risk_level': 'HR',
        'enable_prep': True,
    },
}


def get_pmc9087297_scenario(scenario_name):
    """Get parameters for a specific PMC9087297 scenario.

    Args:
        scenario_name: One of the keys in PMC9087297_SCENARIOS

    Returns:
        Complete parameter dictionary for CEPAC
    """
    if scenario_name not in PMC9087297_SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario_name}. "
                        f"Valid options: {list(PMC9087297_SCENARIOS.keys())}")

    scenario = PMC9087297_SCENARIOS[scenario_name]
    return create_pmc9087297_params(
        risk_level=scenario['risk_level'],
        enable_prep=scenario['enable_prep']
    )


def create_pmc9087297_params(risk_level='VHR', enable_prep=False):
    """Create parameters based on PMC9087297 paper.

    Args:
        risk_level: 'VHR' (very high risk) or 'HR' (high risk)
        enable_prep: Whether to enable PrEP (False = no PrEP baseline)

    Returns:
        Complete parameter dictionary for CEPAC
    """
    # Start with defaults
    params = create_default_params()

    # Get risk-specific parameters
    risk_params = PAPER_PARAMS['hiv_epidemiology'][risk_level]
    monthly_incidence = risk_params['monthly_incidence']
    cd4_at_infection = risk_params['cd4_at_infection']

    prep_suffix = 'GenericPrEP' if enable_prep else 'NoPrEP'

    # === RunSpecs ===
    params['runspecs']['runSetName'] = 'PMC9087297'
    params['runspecs']['runName'] = f'PMC9087297_{risk_level}_{prep_suffix}'
    params['runspecs']['numCohorts'] = 10000
    params['runspecs']['discountFactor'] = PAPER_PARAMS['population']['mean_age_years'] / 1000 + 0.0  # 0.03

    # Use exact paper discount rate
    params['runspecs']['discountFactor'] = PAPER_METADATA['discount_rate']

    # === Cohort Demographics ===
    params['cohort']['initialAgeMean'] = float(PAPER_PARAMS['population']['mean_age_months'])
    params['cohort']['initialAgeStdDev'] = 120.0  # ~10 years SD
    params['cohort']['maleGenderDistribution'] = PAPER_PARAMS['population']['gender_male_pct']
    params['cohort']['initialCD4Mean'] = float(cd4_at_infection)
    params['cohort']['initialCD4StdDev'] = 100.0

    # Initial HVL distribution - all start HIV-negative (HVLvhi = uninfected proxy)
    # Set distribution to highest HVL stratum as placeholder for uninfected
    for cd4_idx in range(CONSTANTS['CD4_NUM_STRATA']):
        params['cohort']['initialHVLDistribution'][cd4_idx] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

    # === HIV Testing ===
    params['hivtest']['enableHIVTesting'] = True
    params['hivtest']['HIVTestSensitivity'] = 0.99
    params['hivtest']['HIVTestSpecificity'] = 0.99
    params['hivtest']['HIVTestCost'] = 50.0
    params['hivtest']['probHIVTestAccept'] = 0.95
    params['hivtest']['probHIVTestReturn'] = 0.95

    # PrEP settings
    if enable_prep:
        params['hivtest']['enablePrEP'] = True
        params['hivtest']['PrEPCostMonthly'] = float(PAPER_PARAMS['costs_2020_usd']['generic_ftdf_monthly'])
        params['hivtest']['PrEPEfficacy'] = 0.99  # ~99% efficacy with good adherence
        params['hivtest']['probPrEPDropout'] = 0.02
    else:
        params['hivtest']['enablePrEP'] = False
        params['hivtest']['PrEPCostMonthly'] = 0.0
        params['hivtest']['PrEPEfficacy'] = 0.0
        params['hivtest']['probPrEPDropout'] = 0.0

    # === ART Treatment ===
    art_monthly_cost = float(PAPER_PARAMS['costs_2020_usd']['art_min_monthly'])
    for art_line in params['arts']['artData']:
        art_line['costMonthly'] = art_monthly_cost
        art_line['costInitial'] = 500.0
        art_line['efficacyTimeHorizon'] = 48
        # CD4 response on suppressive ART
        for resp_type in range(CONSTANTS['CD4_RESPONSE_NUM_TYPES']):
            art_line['CD4ChangeOnSuppARTMean'][resp_type] = [10.0, 5.0, 2.0]
            art_line['CD4ChangeOnSuppARTStdDev'][resp_type] = [5.0, 3.0, 1.0]

    # === QOL Settings ===
    qol_min, qol_max = PAPER_PARAMS['treatment']['qol_on_art_range']
    params['qol']['QOLBaseHIVNegative'] = 1.0
    # Off ART - lower QoL
    params['qol']['QOLBaseHIVPositive'][0] = [0.75, 0.78, 0.80, 0.82, 0.84, 0.85]
    # On ART - QoL 0.83-0.87 by CD4 (low CD4 to high CD4)
    params['qol']['QOLBaseHIVPositive'][1] = [qol_min, 0.84, 0.85, 0.86, qol_max, qol_max]

    # === Cost Settings ===
    n_age = CONSTANTS['COST_AGE_CAT_NUM']
    n_gender = CONSTANTS['GENDER_NUM']
    n_cd4 = CONSTANTS['CD4_NUM_STRATA']

    routine_care_monthly = (PAPER_PARAMS['costs_2020_usd']['routine_hiv_care_min_monthly'] +
                           PAPER_PARAMS['costs_2020_usd']['routine_hiv_care_max_monthly']) / 2

    for age_cat in range(n_age):
        for gender in range(n_gender):
            for cd4 in range(n_cd4):
                # Routine care costs (direct medical = index 0)
                params['costs']['routineCareCostHIVPositive'][1][cd4][gender][age_cat][0] = routine_care_monthly * 0.5
                params['costs']['routineCareCostHIVPositive'][0][cd4][gender][age_cat][0] = routine_care_monthly

    for age_cat in range(n_age):
        params['costs']['CD4TestCost'][age_cat][0] = 50.0
        params['costs']['HVLTestCost'][age_cat][0] = 100.0

    for age_cat in range(n_age):
        for gender in range(n_gender):
            params['costs']['generalMedicineCost'][gender][age_cat][0] = 200.0

    # === Natural History ===
    params['nathist']['HIVDeathRateRatio'] = [5.0, 3.0, 2.0, 1.5, 1.2, 1.0]
    params['nathist']['ARTDeathRateRatio'] = 1.1

    for cd4 in range(CONSTANTS['CD4_NUM_STRATA']):
        for hvl in range(CONSTANTS['HVL_NUM_STRATA']):
            base_decline = 2.0 + hvl * 0.5
            params['nathist']['monthlyCD4DeclineMean'][cd4][hvl] = base_decline
            params['nathist']['monthlyCD4DeclineStdDev'][cd4][hvl] = base_decline * 0.3

    return params


def list_scenarios():
    """Print available scenarios."""
    print("PMC9087297 Scenarios:")
    print("=" * 60)
    for name, info in PMC9087297_SCENARIOS.items():
        print(f"  {name}")
        print(f"    {info['description']}")
        print(f"    Risk: {info['risk_level']}, PrEP: {'Yes' if info['enable_prep'] else 'No'}")
        print()


if __name__ == '__main__':
    list_scenarios()
