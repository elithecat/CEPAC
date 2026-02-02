"""
CEPAC Parameter Schema

Defines all ~400+ parameters for the CEPAC model, organized by input tab.
Each parameter includes:
- type: int, float, bool, str, list, matrix
- default: default value
- keyword: the keyword used in .in files
- description: human-readable description
- constraints: optional validation constraints
"""

# Constants from SimContext.h
CONSTANTS = {
    'AGE_YRS': 101,
    'AGE_STARTING': 0,
    'AGE_MAXIMUM': 100,
    'AGE_CATEGORIES': 20,
    'INIT_AGE_NUM_STRATA': 30,
    'GENDER_NUM': 2,
    'NUM_BOUNDS': 2,
    'NUM_DISCOUNT_RATES': 4,
    'RISK_FACT_NUM': 5,
    'CD4_NUM_STRATA': 6,
    'HVL_NUM_STRATA': 7,
    'OI_NUM': 15,
    'DTH_NUM_CAUSES': 38,
    'DTH_NUM_CAUSES_BASIC': 17,
    'CHRM_NUM': 10,
    'CHRM_AGE_CAT_NUM': 7,
    'CHRM_TIME_PER_NUM': 3,
    'CHRM_ORPHANS_AGE_CAT_NUM': 15,
    'COST_AGE_CAT_NUM': 7,
    'ART_NUM_LINES': 10,
    'ART_NUM_STATES': 2,
    'ART_NUM_SUBREGIMENS': 4,
    'ART_NUM_TOX_SEVERITY': 3,
    'ART_NUM_TOX_PER_SEVERITY': 6,
    'ART_NUM_FAIL_TYPES': 3,
    'ART_NUM_STOP_TYPES': 8,
    'ART_NUM_MTHS_RECORD': 3,
    'PROPH_NUM': 3,
    'PROPH_NUM_TYPES': 2,
    'CD4_RESPONSE_NUM_TYPES': 4,
    'CLINIC_VISITS_NUM': 3,
    'THERAPY_IMPL_NUM': 3,
    'STI_NUM_CYCLES': 5,
    'STI_NUM_PERIODS': 2,
    'TB_NUM_STRAINS': 3,
    'TB_NUM_STATES': 6,
    'TB_NUM_TRACKER': 3,
    'TB_NUM_TESTS': 4,
    'TB_NUM_TREATMENTS': 10,
    'TB_NUM_PROPHS': 5,
    'TB_INFECT_NUM_AGE_CAT': 7,
    'TB_TREATM_STAGE_NUM': 2,
    'HIV_TEST_FREQ_NUM': 5,
    'TEST_ACCEPT_NUM': 3,
    'PEDS_HIV_NUM': 4,
    'PEDS_BF_NUM': 4,
    'PEDS_AGE_CHILD_NUM': 11,
    'PEDS_CD4_PERC_NUM': 8,
    'EID_NUM_ASSAYS': 24,
    'EID_NUM_TESTS': 10,
    'INFANT_HIV_PROPHS_NUM': 4,
    'PEDS_COST_AGE_CAT_NUM': 4,
    'PEDS_ART_COST_AGE_CAT_NUM': 6,
    'ADOLESCENT_NUM_AGES': 18,
    'ADOLESCENT_NUM_ART_AGES': 5,
    'TRANSM_RISK_NUM': 3,
    'TRANSM_RISK_AGE_NUM': 7,
    'RESP_NUM_TYPES': 3,
    'RESP_AGE_CAT_NUM': 7,
    'HET_NUM_OUTCOMES': 10,
    'HET_INTV_NUM_PERIODS': 5,
    'RTC_NUM_COEFF': 5,
    'MAX_NUM_SUBCOHORTS': 25,
    'MAX_NUM_TRACES': 100,
    'COST_NUM_TYPES': 4,
    'INC_REDUC_PERIODS_NUM': 6,
    'AGE_CAT_HIV_INC': 20,
    'OUTPUT_AGE_CAT_NUM': 14,
}

# String constants
CD4_STRATA_STRS = ['CD4vlo', 'CD4_lo', 'CD4mlo', 'CD4mhi', 'CD4_hi', 'CD4vhi']
HVL_STRATA_STRS = ['HVLvlo', 'HVL_lo', 'HVLmlo', 'HVLmed', 'HVLmhi', 'HVL_hi', 'HVLvhi']
GENDER_STRS = ['male', 'female']
TRANSM_RISK_STRS = ['MSM', 'IDU', 'Other']
TB_STRAIN_STRS = ['dsTB', 'mdrTB', 'xdrTB']
TB_STATE_STRS = ['Uninfected', 'Latent', 'ActivePulm', 'ActiveExtrapulm', 'PrevTreated', 'TreatDefault']


def create_default_params():
    """Create a dictionary with all default parameter values."""
    params = {
        'runspecs': create_runspecs_defaults(),
        'output': create_output_defaults(),
        'cohort': create_cohort_defaults(),
        'treatment': create_treatment_defaults(),
        'ltfu': create_ltfu_defaults(),
        'heterogeneity': create_heterogeneity_defaults(),
        'sti': create_sti_defaults(),
        'prophs': create_prophs_defaults(),
        'arts': create_arts_defaults(),
        'nathist': create_nathist_defaults(),
        'chrms': create_chrms_defaults(),
        'costs': create_costs_defaults(),
        'tb': create_tb_defaults(),
        'qol': create_qol_defaults(),
        'hivtest': create_hivtest_defaults(),
        'peds': create_peds_defaults(),
        'pedsarts': create_pedsarts_defaults(),
        'pedscosts': create_pedscosts_defaults(),
        'eid': create_eid_defaults(),
        'adolescent': create_adolescent_defaults(),
        'adolescentarts': create_adolescentarts_defaults(),
    }
    return params


def create_runspecs_defaults():
    """RunSpecs tab defaults."""
    return {
        'runSetName': 'DefaultRunSet',
        'runName': 'run1',
        'numCohorts': 10000,
        'discountFactor': 0.03,
        'maxPatientCD4': 2000.0,
        'monthRecordARTEfficacy': [6, 12, 24],
        'randomSeedByTime': True,
        'userProgramLocale': 'en_US',
        'inputVersion': '20210615',
        'modelVersion': '50d',
        'OIsIncludeTB': False,
        'OINames': [f'OI_{i+1}' for i in range(CONSTANTS['OI_NUM'])],
        'OIsFractionOfBenefit': [1.0] * CONSTANTS['OI_NUM'],
        'severeOIs': [False] * CONSTANTS['OI_NUM'],
        'CD4StrataUpperBounds': [50.0, 100.0, 200.0, 350.0, 500.0],
        'longitLoggingLevel': 0,
        'firstOIsLongitLogging': [0] * CONSTANTS['OI_NUM'],
        'enableOIHistoryLogging': False,
        'numARTFailuresForOIHistoryLogging': 0,
        'CD4BoundsForOIHistoryLogging': [0.0, 2000.0],
        'HVLBoundsForOIHistoryLogging': [0, 6],
        'OIsToExcludeOIHistoryLogging': [False] * CONSTANTS['OI_NUM'],
        'enableMultipleDiscountRates': False,
        'multDiscountRatesCost': [0.0, 0.03, 0.05, 0.07],
        'multDiscountRatesBenefit': [0.0, 0.03, 0.05, 0.07],
    }


def create_output_defaults():
    """Output tab defaults."""
    return {
        'traceNumSelection': 100,
        'enableSubCohorts': False,
        'subCohorts': [0] * CONSTANTS['MAX_NUM_SUBCOHORTS'],
        'enableDetailedCostOutputs': False,
    }


def create_cohort_defaults():
    """Cohort tab defaults."""
    return {
        'initialCD4Mean': 500.0,
        'initialCD4StdDev': 200.0,
        'enableSquareRootTransform': True,
        'initialHVLDistribution': [[0.0] * CONSTANTS['HVL_NUM_STRATA']
                                   for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'initialAgeMean': 360.0,  # 30 years in months
        'initialAgeStdDev': 120.0,
        'useCustomAgeDist': False,
        'ageStrata': [0.0] * (2 * CONSTANTS['INIT_AGE_NUM_STRATA']),
        'ageProbs': [0.0] * CONSTANTS['INIT_AGE_NUM_STRATA'],
        'maleGenderDistribution': 0.5,
        'OIProphNonComplianceRisk': 0.0,
        'OIProphNonComplianceDegree': 0.0,
        'clinicVisitTypeDistribution': [0.0, 0.0, 1.0],
        'therapyImplementationDistribution': [0.0, 0.0, 1.0],
        'CD4ResponseTypeOnARTDistribution': [0.25, 0.25, 0.25, 0.25],
        'probOIHistoryAtEntry': [[[0.0] * CONSTANTS['OI_NUM']
                                  for _ in range(CONSTANTS['HVL_NUM_STRATA'])]
                                 for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'probRiskFactorPrev': [0.0] * CONSTANTS['RISK_FACT_NUM'],
        'probRiskFactorIncid': [0.0] * CONSTANTS['RISK_FACT_NUM'],
        'riskFactorNames': [f'Risk_{i+1}' for i in range(CONSTANTS['RISK_FACT_NUM'])],
        'showTransmissionOutput': False,
        'transmRateOnART': [[0.0] * CONSTANTS['HVL_NUM_STRATA']
                           for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'transmRateOnARTAcute': [0.0] * CONSTANTS['CD4_NUM_STRATA'],
        'transmRateOffART': [[0.0] * CONSTANTS['HVL_NUM_STRATA']
                            for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'transmRateOffARTAcute': [0.0] * CONSTANTS['CD4_NUM_STRATA'],
        'transmUseHIVTestAcuteDefinition': False,
        'transmAcuteDuration': 3,
        'transmRateMultInterval': [12, 24],
        'transmRateMult': [1.0, 1.0, 1.0],
        'transmRiskDistrib': [[[1.0/3] * CONSTANTS['TRANSM_RISK_NUM']
                              for _ in range(CONSTANTS['TRANSM_RISK_AGE_NUM'])]
                             for _ in range(CONSTANTS['GENDER_NUM'])],
        'transmRiskMultBounds': [12, 24],
        'transmRiskMult': [[1.0, 1.0, 1.0] for _ in range(CONSTANTS['TRANSM_RISK_NUM'])],
        'useDynamicTransm': False,
        'dynamicTransmHRGTransmissions': 0.0,
        'dynamicTransmPropHRGAttributable': 0.0,
        'dynamicTransmNumHIVPosHRG': 0.0,
        'dynamicTransmNumHIVNegHRG': 0.0,
        'dynamicTransmWarmupSize': 0,
        'keepPrEPAfterWarmup': False,
        'usePrEPDuringWarmup': False,
        'useTransmEndLifeHVLAdjustment': False,
        'transmEndLifeHVLAdjustmentCD4Threshold': 0.0,
        'transmEndLifeHVLAdjustmentARTLineThreshold': 0,
    }


def create_treatment_defaults():
    """Treatment tab defaults."""
    n_lines = CONSTANTS['ART_NUM_LINES']
    n_ois = CONSTANTS['OI_NUM']

    # ART start policy defaults
    def default_art_start():
        return {
            'CD4BoundsOnly': [-1.0, -1.0],
            'HVLBoundsOnly': [-1, -1],
            'CD4BoundsWithHVL': [-1.0, -1.0],
            'HVLBoundsWithCD4': [-1, -1],
            'OIHistory': [False] * n_ois,
            'numOIs': 0,
            'CD4BoundsWithOIs': [-1.0, -1.0],
            'OIHistoryWithCD4': [False] * n_ois,
            'ensureSuppFalsePositiveFailure': False,
            'minMonthNum': 0,
            'maxMonthNum': -1,
            'monthsSincePrevRegimen': 0,
        }

    # ART fail policy defaults
    def default_art_fail():
        return {
            'HVLNumIncrease': -1,
            'HVLBounds': [-1, -1],
            'HVLFailAtSetpoint': False,
            'HVLMonthsFromInit': 0,
            'CD4PercentageDrop': -1.0,
            'CD4BelowPreARTNadir': False,
            'CD4BoundsOR': [-1.0, -1.0],
            'CD4BoundsAND': [-1.0, -1.0],
            'CD4MonthsFromInit': 0,
            'OIsEvent': [0] * n_ois,
            'OIsMinNum': 0,
            'OIsMonthsFromInit': 0,
            'diagnoseNumTestsFail': 1,
            'diagnoseUseHVLTestsConfirm': False,
            'diagnoseUseCD4TestsConfirm': False,
            'diagnoseNumTestsConfirm': 0,
        }

    # ART stop policy defaults
    def default_art_stop():
        return {
            'maxMonthsOnART': -1,
            'withMajorToxicity': False,
            'afterFailImmediate': False,
            'afterFailCD4LowerBound': -1.0,
            'afterFailWithSevereOI': False,
            'afterFailMonthsFromObserved': -1,
            'afterFailMinMonthNum': 0,
            'afterFailMonthsFromInit': -1,
            'nextLineAfterMajorTox': -1,
        }

    # Proph start/stop policy defaults
    def default_proph_start():
        return {
            'useOrEvaluation': False,
            'currCD4Bounds': [-1.0, -1.0],
            'minCD4Bounds': [-1.0, -1.0],
            'OIHistory': [0] * n_ois,
            'minMonthNum': 0,
        }

    def default_proph_stop():
        return {
            'useOrEvaluation': False,
            'currCD4Bounds': [-1.0, -1.0],
            'minCD4Bounds': [-1.0, -1.0],
            'OIHistory': [0] * n_ois,
            'minMonthNum': 0,
            'monthsOnProph': -1,
        }

    return {
        'clinicVisitInterval': 3,
        'probDetectOIAtEntry': [0.0] * n_ois,
        'probDetectOISinceLastVisit': [0.0] * n_ois,
        'probSwitchSecondaryProph': [0.0] * n_ois,
        'testingIntervalCD4Threshold': 200.0,
        'testingIntervalARTMonthsThreshold': 6,
        'testingIntervalLastARTMonthsThreshold': 6,
        'CD4TestingIntervalPreARTHighCD4': 6,
        'CD4TestingIntervalPreARTLowCD4': 3,
        'CD4TestingIntervalOnART': [3, 6],
        'CD4TestingIntervalOnLastART': [3, 6],
        'CD4TestingIntervalPostART': 6,
        'HVLTestingIntervalPreARTHighCD4': 6,
        'HVLTestingIntervalPreARTLowCD4': 3,
        'HVLTestingIntervalOnART': [3, 6],
        'HVLTestingIntervalOnLastART': [3, 6],
        'HVLTestingIntervalPostART': 6,
        'probHVLTestErrorHigher': 0.0,
        'probHVLTestErrorLower': 0.0,
        'CD4TestStdDevPercentage': 0.15,
        'CD4TestBiasMean': 0.0,
        'CD4TestBiasStdDevPercentage': 0.0,
        'ARTFailureOnlyAtRegularVisit': True,
        'numARTInitialHVLTests': 0,
        'numARTInitialCD4Tests': 0,
        'emergencyVisitIsNotRegularVisit': False,
        'CD4TestingLag': 0,
        'HVLTestingLag': 0,
        'cd4MonitoringStopEnable': False,
        'cd4MonitoringStopThreshold': 0.0,
        'cd4MonitoringStopMthsPostARTInit': 0,
        'startART': [default_art_start() for _ in range(n_lines)],
        'enableSTIForART': [False] * n_lines,
        'failART': [default_art_fail() for _ in range(n_lines)],
        'stopART': [default_art_stop() for _ in range(n_lines)],
        'ARTResistancePriorRegimen': [[0.0] * n_lines for _ in range(n_lines)],
        'ARTResistanceHVL': [0.0] * CONSTANTS['HVL_NUM_STRATA'],
        'startProph': [[default_proph_start() for _ in range(n_ois)]
                       for _ in range(CONSTANTS['PROPH_NUM_TYPES'])],
        'stopProph': [[default_proph_stop() for _ in range(n_ois)]
                      for _ in range(CONSTANTS['PROPH_NUM_TYPES'])],
    }


def create_ltfu_defaults():
    """LTFU tab defaults."""
    return {
        'useLTFU': False,
        'propRespondLTFUPreARTLogitMean': 0.0,
        'propRespondLTFUPreARTLogitStdDev': 0.0,
        'useInterventionLTFU': False,
        'responseThresholdLTFU': [0.0, 0.0],
        'responseValueLTFU': [0.0, 0.0],
        'responseThresholdPeriodLTFU': [[0.0, 0.0] for _ in range(CONSTANTS['HET_INTV_NUM_PERIODS'])],
        'responseValuePeriodLTFU': [[0.0, 0.0] for _ in range(CONSTANTS['HET_INTV_NUM_PERIODS'])],
        'responseThresholdLTFUOffIntervention': [0.0, 0.0],
        'responseValueLTFUOffIntervention': [0.0, 0.0],
        'propGeneralMedicineCost': [0.0] * 6,  # HIV_CARE_NUM
        'propInterventionCost': [0.0] * 6,
        'probRemainOnOIProph': 0.0,
        'probRemainOnOITreatment': 0.0,
        'minMonthsRemainLost': 1,
        'regressionCoefficientsRTC': [0.0] * CONSTANTS['RTC_NUM_COEFF'],
        'CD4ThresholdRTC': 0.0,
        'severeOIsRTC': [False] * CONSTANTS['OI_NUM'],
        'maxMonthsAfterObservedFailureToRestartRegimen': -1,
        'probRestartRegimenWithoutObservedFailure': 0.0,
        'recheckARTStartPoliciesAtRTC': False,
        'useProbSuppByPrevOutcome': False,
        'probSuppressionWhenReturnToFailed': [0.0] * CONSTANTS['ART_NUM_LINES'],
        'probSuppressionWhenReturnToSuppressed': [0.0] * CONSTANTS['ART_NUM_LINES'],
        'probResumeInterventionRTC': 0.0,
        'costResumeInterventionRTC': 0.0,
    }


def create_heterogeneity_defaults():
    """Heterogeneity tab defaults."""
    return {
        'propRespondBaselineLogitMean': 0.0,
        'propRespondBaselineLogitStdDev': 0.0,
        'propRespondAge': [0.0] * CONSTANTS['RESP_AGE_CAT_NUM'],
        'propRespondAgeEarly': 0.0,
        'propRespondAgeLate': 0.0,
        'propRespondCD4': [0.0] * CONSTANTS['CD4_NUM_STRATA'],
        'propRespondFemale': 0.0,
        'propRespondHistoryOIs': 0.0,
        'propRespondPriorARTToxicity': 0.0,
        'propRespondRiskFactor': [0.0] * CONSTANTS['RISK_FACT_NUM'],
        'useIntervention': [False] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionDurationMean': [0.0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionDurationSD': [0.0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionAdjustmentMean': [0.0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionAdjustmentSD': [0.0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionAdjustmentDistribution': [0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionCostInit': [0.0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
        'interventionCostMonthly': [0.0] * CONSTANTS['HET_INTV_NUM_PERIODS'],
    }


def create_sti_defaults():
    """STI tab defaults."""
    n_lines = CONSTANTS['ART_NUM_LINES']

    def default_initiation():
        return {
            'CD4BoundsOnly': [-1.0, -1.0],
            'HVLBoundsOnly': [-1, -1],
            'CD4BoundsWithHVL': [-1.0, -1.0],
            'HVLBoundsWithCD4': [-1, -1],
            'OIHistory': [False] * CONSTANTS['OI_NUM'],
            'numOIs': 0,
            'CD4BoundsWithOIs': [-1.0, -1.0],
            'OIHistoryWithCD4': [False] * CONSTANTS['OI_NUM'],
            'minMonthNum': 0,
            'maxMonthNum': -1,
            'monthsSincePrevRegimen': 0,
            'monthsSinceARTStart': 0,
        }

    def default_endpoint():
        return {
            'CD4BoundsOnly': [-1.0, -1.0],
            'HVLBoundsOnly': [-1, -1],
            'CD4BoundsWithHVL': [-1.0, -1.0],
            'HVLBoundsWithCD4': [-1, -1],
            'OIHistory': [False] * CONSTANTS['OI_NUM'],
            'numOIs': 0,
            'CD4BoundsWithOIs': [-1.0, -1.0],
            'OIHistoryWithCD4': [False] * CONSTANTS['OI_NUM'],
            'minMonthNum': 0,
            'maxMonthNum': -1,
            'monthsSincePrevRegimen': 0,
            'monthsSinceSTIStart': 0,
        }

    return {
        'firstInterruption': [default_initiation() for _ in range(n_lines)],
        'ARTRestartCD4Bounds': [[-1.0, -1.0] for _ in range(n_lines)],
        'ARTRestartHVLBounds': [[-1, -1] for _ in range(n_lines)],
        'ARTRestartFirstTestMonth': 0,
        'ARTRestartSecondTestMonth': 0,
        'ARTRestartTestInterval': 0,
        'ARTRestopCD4Bounds': [[-1.0, -1.0] for _ in range(n_lines)],
        'ARTRestopHVLBounds': [[-1, -1] for _ in range(n_lines)],
        'ARTRestopFirstTestMonth': 0,
        'ARTRestopSecondTestMonth': 0,
        'ARTRestopTestInterval': 0,
        'endpoint': [default_endpoint() for _ in range(n_lines)],
    }


def create_prophs_defaults():
    """Prophs tab defaults - per proph type x OI x proph line."""
    def default_proph():
        return {
            'primaryOIEfficacy': [0.0] * CONSTANTS['OI_NUM'],
            'secondaryOIEfficacy': [0.0] * CONSTANTS['OI_NUM'],
            'monthlyProbResistance': 0.0,
            'percentResistance': 0.0,
            'timeOfResistance': 0,
            'costFactorResistance': 1.0,
            'deathRateRatioResistance': 1.0,
            'probMinorToxicity': 0.0,
            'probMajorToxicity': 0.0,
            'monthsToToxicity': 0,
            'deathRateRatioMajorToxicity': 1.0,
            'costMonthly': 0.0,
            'costMinorToxicity': 0.0,
            'QOLMinorToxicity': 1.0,
            'costMajorToxicity': 0.0,
            'QOLMajorToxicity': 1.0,
            'monthsToSwitch': -1,
            'switchOnMinorToxicity': False,
            'switchOnMajorToxicity': False,
        }

    # [proph_type][oi][proph_line]
    return {
        'prophData': [[[default_proph() for _ in range(CONSTANTS['PROPH_NUM'])]
                       for _ in range(CONSTANTS['OI_NUM'])]
                      for _ in range(CONSTANTS['PROPH_NUM_TYPES'])]
    }


def create_arts_defaults():
    """ARTs tab defaults - per ART line."""
    def default_toxicity():
        return {
            'toxicityName': '',
            'probToxicity': 0.0,
            'timeToToxicityMean': 0.0,
            'timeToToxicityStdDev': 0.0,
            'QOLModifier': 1.0,
            'QOLDuration': 0,
            'costAmount': 0.0,
            'costDuration': 0,
            'switchARTRegimenOnToxicity': -1,
            'switchSubRegimenOnToxicity': -1,
            'timeToChronicDeathImpact': 0,
            'chronicToxDeathRateRatio': 1.0,
            'chronicDeathDuration': 0,
            'acuteMajorToxDeathRateRatio': 1.0,
            'costAcuteDeathMajorToxicity': 0.0,
        }

    def default_art_line():
        return {
            'costInitial': 0.0,
            'costMonthly': 0.0,
            'efficacyTimeHorizon': 48,
            'efficacyTimeHorizonResuppression': 48,
            'forceFailAtMonth': -1,
            'stageBoundsCD4ChangeOnSuppART': [6, 24],
            'stageBoundCD4ChangeOnARTFail': 24,
            'CD4ChangeOnSuppARTMean': [[0.0, 0.0, 0.0] for _ in range(CONSTANTS['CD4_RESPONSE_NUM_TYPES'])],
            'CD4ChangeOnSuppARTStdDev': [[0.0, 0.0, 0.0] for _ in range(CONSTANTS['CD4_RESPONSE_NUM_TYPES'])],
            'CD4MultiplierOnFailedART': [[1.0, 1.0] for _ in range(CONSTANTS['CD4_RESPONSE_NUM_TYPES'])],
            'secondaryCD4ChangeOnARTStdDev': 0.0,
            'monthlyCD4MultiplierOffARTPreSetpoint': [1.0, 1.0],
            'monthlyCD4MultiplierOffARTPostSetpoint': [1.0, 1.0],
            'monthlyProbHVLChange': [0.0, 0.0],
            'monthlyNumStrataHVLChange': [0, 0],
            'toxicity': [[[default_toxicity() for _ in range(CONSTANTS['ART_NUM_TOX_PER_SEVERITY'])]
                          for _ in range(CONSTANTS['ART_NUM_TOX_SEVERITY'])]
                         for _ in range(CONSTANTS['ART_NUM_SUBREGIMENS'])],
            'monthsToSwitchSubRegimen': [-1] * CONSTANTS['ART_NUM_SUBREGIMENS'],
            'propMthCostNonResponders': 1.0,
            'probRestartARTRegimenAfterFailure': [0.0] * CONSTANTS['RESP_NUM_TYPES'],
            'maxRestartAttempts': 0,
            'propRespondARTRegimenLogitMean': 0.0,
            'propRespondARTRegimenLogitStdDev': 0.0,
            'propRespondARTRegimenLogitDistribution': 0,
            'propRespondARTRegimenUseDuration': False,
            'propRespondARTRegimenDurationMean': 0.0,
            'propRespondARTRegimenDurationStdDev': 0.0,
            'responseTypeThresholds': [[0.0, 0.0] for _ in range(CONSTANTS['HET_NUM_OUTCOMES'])],
            'responseTypeValues': [[0.0, 0.0] for _ in range(CONSTANTS['HET_NUM_OUTCOMES'])],
            'responseTypeExponents': [1.0] * CONSTANTS['HET_NUM_OUTCOMES'],
            'applyARTEffectOnFailed': False,
        }

    return {
        'artData': [default_art_line() for _ in range(CONSTANTS['ART_NUM_LINES'])]
    }


def create_nathist_defaults():
    """NatHist tab defaults."""
    return {
        'HIVDeathRateRatio': [1.0] * CONSTANTS['CD4_NUM_STRATA'],
        'ARTDeathRateRatio': 1.0,
        'monthlyOIProbOffART': [[[0.0] * 2 for _ in range(CONSTANTS['OI_NUM'])]
                                for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'monthlyOIProbOnARTMult': [[1.0] * CONSTANTS['OI_NUM']
                                   for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'acuteOIDeathRateRatio': [1.0] * CONSTANTS['CD4_NUM_STRATA'],
        'acuteOIDeathRateRatioTB': [1.0] * CONSTANTS['CD4_NUM_STRATA'],
        'severeOIHistDeathRateRatio': 1.0,
        'severeOIHistEffectDuration': 0,
        'TB_OIHistDeathRateRatio': 1.0,
        'TB_OIHistEffectDuration': 0,
        'genericRiskDeathRateRatio': [1.0] * CONSTANTS['RISK_FACT_NUM'],
        'monthlyCD4DeclineMean': [[0.0] * CONSTANTS['HVL_NUM_STRATA']
                                  for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'monthlyCD4DeclineStdDev': [[0.0] * CONSTANTS['HVL_NUM_STRATA']
                                    for _ in range(CONSTANTS['CD4_NUM_STRATA'])],
        'monthlyCD4DeclineBtwSubject': 0.0,
        'monthlyBackgroundDeathRate': [[0.0] * CONSTANTS['AGE_YRS']
                                        for _ in range(CONSTANTS['GENDER_NUM'])],
        'backgroundMortModifierType': 0,
        'backgroundMortModifier': 0.0,
    }


def create_chrms_defaults():
    """CHRMs tab defaults."""
    return {
        'showCHRMsOutput': False,
        'CHRMNames': [f'CHRM_{i+1}' for i in range(CONSTANTS['CHRM_NUM'])],
        'enableOrphans': False,
        'showOrphansOutput': False,
        'ageBounds': [[0] * (CONSTANTS['CHRM_AGE_CAT_NUM'] - 1)
                      for _ in range(CONSTANTS['CHRM_NUM'])],
        'durationCHRMSstage': [[[0.0, 0.0] for _ in range(CONSTANTS['CHRM_NUM'])]
                               for _ in range(CONSTANTS['CHRM_TIME_PER_NUM'] - 1)],
        'enableCHRMSDurationSqrtTransform': False,
        'probPrevalentCHRMsHIVneg': [[[0.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                                      for _ in range(CONSTANTS['GENDER_NUM'])]
                                     for _ in range(CONSTANTS['CHRM_NUM'])],
        'probPrevalentCHRMs': [[[[0.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                                 for _ in range(CONSTANTS['GENDER_NUM'])]
                                for _ in range(CONSTANTS['CD4_NUM_STRATA'])]
                               for _ in range(CONSTANTS['CHRM_NUM'])],
        'probPrevalentCHRMsRiskFactorLogit': [[0.0] * CONSTANTS['RISK_FACT_NUM']
                                               for _ in range(CONSTANTS['CHRM_NUM'])],
        'prevalentCHRMsMonthsSinceStartMean': [0.0] * CONSTANTS['CHRM_NUM'],
        'prevalentCHRMsMonthsSinceStartStdDev': [0.0] * CONSTANTS['CHRM_NUM'],
        'prevalentCHRMsMonthsSinceStartOrphans': [[0] * CONSTANTS['CHRM_ORPHANS_AGE_CAT_NUM']
                                                   for _ in range(CONSTANTS['CHRM_NUM'])],
        'incidentCHRMsMonthsSincePreviousOrphans': 0,
        'probIncidentCHRMsHIVneg': [[[0.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                                     for _ in range(CONSTANTS['GENDER_NUM'])]
                                    for _ in range(CONSTANTS['CHRM_NUM'])],
        'probIncidentCHRMs': [[[[0.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                                for _ in range(CONSTANTS['GENDER_NUM'])]
                               for _ in range(CONSTANTS['CD4_NUM_STRATA'])]
                              for _ in range(CONSTANTS['CHRM_NUM'])],
        'probIncidentCHRMsOnARTMult': [[1.0] * CONSTANTS['CD4_NUM_STRATA']
                                        for _ in range(CONSTANTS['CHRM_NUM'])],
        'probIncidentCHRMsRiskFactorLogit': [[0.0] * CONSTANTS['RISK_FACT_NUM']
                                              for _ in range(CONSTANTS['CHRM_NUM'])],
        'probIncidentCHRMsPriorHistoryLogit': [[0.0] * CONSTANTS['CHRM_NUM']
                                                for _ in range(CONSTANTS['CHRM_NUM'])],
        'CHRMsDeathRateRatio': [[[[1.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                                  for _ in range(CONSTANTS['GENDER_NUM'])]
                                 for _ in range(CONSTANTS['CHRM_TIME_PER_NUM'])]
                                for _ in range(CONSTANTS['CHRM_NUM'])],
        'costCHRMs': [[[[0.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                        for _ in range(CONSTANTS['GENDER_NUM'])]
                       for _ in range(CONSTANTS['CHRM_TIME_PER_NUM'])]
                      for _ in range(CONSTANTS['CHRM_NUM'])],
        'costDeathCHRMs': [0.0] * CONSTANTS['CHRM_NUM'],
        'QOLModCHRMs': [[[[1.0] * CONSTANTS['CHRM_AGE_CAT_NUM']
                          for _ in range(CONSTANTS['GENDER_NUM'])]
                         for _ in range(CONSTANTS['CHRM_TIME_PER_NUM'])]
                        for _ in range(CONSTANTS['CHRM_NUM'])],
        'QOLModDeathCHRMs': [1.0] * CONSTANTS['CHRM_NUM'],
        'QOLModMultipleCHRMs': [1.0] * (CONSTANTS['CHRM_NUM'] - 1),
    }


def create_costs_defaults():
    """Costs tab defaults."""
    n_age = CONSTANTS['COST_AGE_CAT_NUM']
    n_art = CONSTANTS['ART_NUM_STATES']
    n_oi = CONSTANTS['OI_NUM']
    n_dth = CONSTANTS['DTH_NUM_CAUSES_BASIC']
    n_cost = CONSTANTS['COST_NUM_TYPES']
    n_gender = CONSTANTS['GENDER_NUM']
    n_cd4 = CONSTANTS['CD4_NUM_STRATA']

    return {
        'costAgeBounds': [18, 25, 35, 45, 55, 65],
        'acuteOICostTreated': [[[[0.0] * n_cost for _ in range(n_oi)]
                                for _ in range(n_art)]
                               for _ in range(n_age)],
        'acuteOICostUntreated': [[[[0.0] * n_cost for _ in range(n_oi)]
                                  for _ in range(n_art)]
                                 for _ in range(n_age)],
        'CD4TestCost': [[0.0] * n_cost for _ in range(n_age)],
        'HVLTestCost': [[0.0] * n_cost for _ in range(n_age)],
        'deathCostTreated': [[[[0.0] * n_cost for _ in range(n_dth)]
                              for _ in range(n_art)]
                             for _ in range(n_age)],
        'deathCostUntreated': [[[[0.0] * n_cost for _ in range(n_dth)]
                                for _ in range(n_art)]
                               for _ in range(n_age)],
        'generalMedicineCost': [[[0.0] * n_cost for _ in range(n_age)]
                                 for _ in range(n_gender)],
        'routineCareCostHIVPositive': [[[[[0.0] * n_cost for _ in range(n_age)]
                                         for _ in range(n_gender)]
                                        for _ in range(n_cd4)]
                                       for _ in range(n_art)],
        'routineCareCostHIVNegative': [[[0.0] * n_cost for _ in range(n_age)]
                                        for _ in range(n_gender)],
        'routineCareCostHIVPositiveUndetected': [[[0.0] * n_cost for _ in range(n_age)]
                                                  for _ in range(n_gender)],
        'routineCareCostHIVNegativeStopAge': 100,
        'routineCareCostHIVPositiveUndetectedStopAge': 100,
        'clinicVisitCostRoutine': [[[[0.0] * n_cost for _ in range(n_cd4)]
                                    for _ in range(n_gender)]
                                   for _ in range(n_age)],
    }


def create_tb_defaults():
    """TB tab defaults."""
    n_strains = CONSTANTS['TB_NUM_STRAINS']
    n_states = CONSTANTS['TB_NUM_STATES']
    n_cd4 = CONSTANTS['CD4_NUM_STRATA']
    n_tests = CONSTANTS['TB_NUM_TESTS']
    n_treatments = CONSTANTS['TB_NUM_TREATMENTS']
    n_prophs = CONSTANTS['TB_NUM_PROPHS']

    def default_tb_proph():
        return {
            'efficacyInfectionHIVNeg': [0.0, 0.0],
            'efficacyInfectionHIVPos': [[0.0, 0.0] for _ in range(n_cd4)],
            'monthsOfEfficacyInfection': 0,
            'decayPeriodInfection': 0,
            'efficacyActivationHIVNeg': [[0.0, 0.0] for _ in range(n_strains)],
            'efficacyActivationHIVPos': [[[0.0, 0.0] for _ in range(n_cd4)] for _ in range(n_strains)],
            'monthsOfEfficacyActivation': [0] * n_strains,
            'decayPeriodActivation': [0] * n_strains,
            'efficacyReinfectionHIVNeg': [[0.0, 0.0] for _ in range(n_strains)],
            'efficacyReinfectionHIVPos': [[[0.0, 0.0] for _ in range(n_cd4)] for _ in range(n_strains)],
            'monthsOfEfficacyReinfection': [0] * n_strains,
            'decayPeriodReinfection': [0] * n_strains,
            'costMonthly': 0.0,
            'costMinorToxicity': 0.0,
            'QOLModifierMinorToxicity': 1.0,
            'costMajorToxicity': 0.0,
            'QOLModifierMajorToxicity': 1.0,
            'probMinorToxicityHIVNeg': 0.0,
            'probMinorToxicityOffART': 0.0,
            'probMinorToxicityOnART': 0.0,
            'probMajorToxicityHIVNeg': 0.0,
            'probMajorToxicityOffART': 0.0,
            'probMajorToxicityOnART': 0.0,
            'deathRateRatioMajorToxicity': 1.0,
            'probResistanceInActiveStates': 0.0,
        }

    def default_tb_test():
        return {
            'probPositiveHIVNeg': [0.0] * n_states,
            'probPositiveHIVPos': [[0.0] * n_cd4 for _ in range(n_states)],
            'probAccept': 1.0,
            'probPickup': 1.0,
            'monthsToReset': 0,
            'timeToPickupMean': 0.0,
            'timeToPickupStdDev': 0.0,
            'DSTMatrixObsvTrue': [[0.0] * n_strains for _ in range(n_strains)],
            'DSTMonthsToResult': [0] * n_strains,
            'DSTLinked': False,
            'DSTProbPickup': 1.0,
            'initCost': 0.0,
            'QOLMod': 1.0,
            'DSTCost': 0.0,
        }

    def default_tb_treatment():
        return {
            'stage1Duration': 2,
            'totalDuration': 6,
            'costInitial': 0.0,
            'costMonthly': [0.0, 0.0],
            'probSuccessHIVNeg': [0.0] * n_strains,
            'probSuccessHIVPos': [[0.0] * n_cd4 for _ in range(n_strains)],
            'probMinorToxHIVNeg': [0.0, 0.0],
            'probMajorToxHIVNeg': [0.0, 0.0],
            'probMinorToxOffARTHIVPos': [0.0, 0.0],
            'probMajorToxOffARTHIVPos': [0.0, 0.0],
            'probMinorToxOnARTHIVPos': [0.0, 0.0],
            'probMajorToxOnARTHIVPos': [0.0, 0.0],
            'costMinorToxicity': 0.0,
            'QOLModifierMinorToxicity': 1.0,
            'costMajorToxicity': 0.0,
            'QOLModifierMajorToxicity': 1.0,
            'deathRateRatioMajorToxicity': 1.0,
        }

    return {
        'enableTB': False,
        'tbProphs': [default_tb_proph() for _ in range(n_prophs)],
        'tbTests': [default_tb_test() for _ in range(n_tests)],
        'tbTreatments': [default_tb_treatment() for _ in range(n_treatments)],
    }


def create_qol_defaults():
    """QOL tab defaults."""
    return {
        'QOLCalculationType': 0,  # MULT
        'QOLBaseHIVNegative': 1.0,
        'QOLBaseHIVPositive': [[1.0] * CONSTANTS['CD4_NUM_STRATA']
                               for _ in range(CONSTANTS['ART_NUM_STATES'])],
        'QOLAcuteOI': [1.0] * CONSTANTS['OI_NUM'],
        'QOLDeathMonth': 0.0,
    }


def create_hivtest_defaults():
    """HIVTest tab defaults."""
    return {
        'enableHIVTesting': False,
        'HIVTestSensitivity': 0.99,
        'HIVTestSpecificity': 0.99,
        'HIVTestCost': 0.0,
        'probHIVTestAccept': 1.0,
        'probHIVTestReturn': 1.0,
        'monthsToHIVTestReturn': 0,
        'enablePrEP': False,
        'PrEPCostMonthly': 0.0,
        'PrEPEfficacy': 0.0,
        'probPrEPDropout': 0.0,
    }


def create_peds_defaults():
    """Peds tab defaults."""
    return {
        'enablePediatrics': False,
        'probPedsHIVPosAtEntry': [0.0] * 3,  # IU, IP, PP
        'pedsInitialCD4PercMean': 0.25,
        'pedsInitialCD4PercStdDev': 0.1,
    }


def create_pedsarts_defaults():
    """PedsARTs tab defaults."""
    return {
        'pedsARTData': [{
            'costInitial': 0.0,
            'costMonthly': 0.0,
        } for _ in range(CONSTANTS['ART_NUM_LINES'])]
    }


def create_pedscosts_defaults():
    """PedsCosts tab defaults."""
    return {
        'pedsCD4TestCost': [0.0] * CONSTANTS['PEDS_COST_AGE_CAT_NUM'],
        'pedsHVLTestCost': [0.0] * CONSTANTS['PEDS_COST_AGE_CAT_NUM'],
    }


def create_eid_defaults():
    """EID tab defaults."""
    return {
        'enableEID': False,
        'eidTestCost': [0.0] * CONSTANTS['EID_NUM_TESTS'],
        'eidTestSensitivity': [[0.0] * 18 for _ in range(CONSTANTS['EID_NUM_TESTS'])],
        'eidTestSpecificity': [[1.0] * 18 for _ in range(CONSTANTS['EID_NUM_TESTS'])],
    }


def create_adolescent_defaults():
    """Adolescent tab defaults."""
    return {
        'enableAdolescent': False,
        'adolescentAgeBounds': [10, 15, 20],
    }


def create_adolescentarts_defaults():
    """AdolescentARTs tab defaults."""
    return {
        'adolescentARTData': [{
            'costInitial': 0.0,
            'costMonthly': 0.0,
        } for _ in range(CONSTANTS['ART_NUM_LINES'])]
    }


# Keyword mapping for .in file parsing
# Maps keywords to (tab, path) tuples
KEYWORD_MAP = {
    # RunSpecs
    'Runset': ('runspecs', 'runSetName'),
    'CohortSize': ('runspecs', 'numCohorts'),
    'DiscFactor': ('runspecs', 'discountFactor'),
    'MaxPatCD4': ('runspecs', 'maxPatientCD4'),
    'MthRecARTEffA': ('runspecs', 'monthRecordARTEfficacy[0]'),
    'MthRecARTEffB': ('runspecs', 'monthRecordARTEfficacy[1]'),
    'MthRecARTEffC': ('runspecs', 'monthRecordARTEfficacy[2]'),
    'RandSeedByTime': ('runspecs', 'randomSeedByTime'),
    'UserLocale': ('runspecs', 'userProgramLocale'),
    'InpVer': ('runspecs', 'inputVersion'),
    'ModelVer': ('runspecs', 'modelVersion'),
    'IncludeTB_AsOI': ('runspecs', 'OIsIncludeTB'),
    'OIstrs': ('runspecs', 'OINames'),
    'LongitLogCohort': ('runspecs', 'longitLoggingLevel'),
    'LongitLogFirstOIs': ('runspecs', 'firstOIsLongitLogging'),
    'LogPriorOIHistProb': ('runspecs', 'enableOIHistoryLogging'),
    'LogOIHistwithARTfails': ('runspecs', 'numARTFailuresForOIHistoryLogging'),
    'LogOIHistwithCD4': ('runspecs', 'CD4BoundsForOIHistoryLogging'),
    'LogOIHistwithHVL': ('runspecs', 'HVLBoundsForOIHistoryLogging'),
    'LogOIHistExcludeOITypes': ('runspecs', 'OIsToExcludeOIHistoryLogging'),
    'FOB_OIs': ('runspecs', 'OIsFractionOfBenefit'),
    'Severe_OIs': ('runspecs', 'severeOIs'),
    'CD4Bounds': ('runspecs', 'CD4StrataUpperBounds'),
    'EnableMultDiscountOutput': ('runspecs', 'enableMultipleDiscountRates'),
    'DiscountRatesCost': ('runspecs', 'multDiscountRatesCost'),
    'DiscountRatesBenefit': ('runspecs', 'multDiscountRatesBenefit'),

    # Output
    'NumPatientsToTrace': ('output', 'traceNumSelection'),
    'EnableSubCohorts': ('output', 'enableSubCohorts'),
    'SubCohortValues': ('output', 'subCohorts'),
    'EnableDetailedCosts': ('output', 'enableDetailedCostOutputs'),

    # Cohort
    'InitCD4': ('cohort', 'initialCD4'),
    'UseSqRtTransform': ('cohort', 'enableSquareRootTransform'),
    'InitHVL': ('cohort', 'initialHVLDistribution'),
    'InitAge': ('cohort', 'initialAge'),
    'InitAgeCustomDist': ('cohort', 'useCustomAgeDist'),
    'AgeStratMins': ('cohort', 'ageStrata'),
    'AgeStratMaxes': ('cohort', 'ageStrata'),
    'AgeStratProbs': ('cohort', 'ageProbs'),
    'InitGender': ('cohort', 'maleGenderDistribution'),
    'ProphNonCompliance': ('cohort', 'OIProphNonCompliance'),
    'PatClinicTypes': ('cohort', 'clinicVisitTypeDistribution'),
    'PatTreatmentTypes': ('cohort', 'therapyImplementationDistribution'),
    'PatCD4ResponeTypeOnART': ('cohort', 'CD4ResponseTypeOnARTDistribution'),
    'PriorOIHistAtEntry': ('cohort', 'probOIHistoryAtEntry'),
    'ProbRiskFactorPrev': ('cohort', 'probRiskFactorPrev'),
    'ProbRiskFactorIncid': ('cohort', 'probRiskFactorIncid'),
    'GenRiskFactorStrs': ('cohort', 'riskFactorNames'),

    # Treatment (partial - there are many more)
    'IntvlClinicVisit': ('treatment', 'clinicVisitInterval'),
    'ProbDetOI_Entry': ('treatment', 'probDetectOIAtEntry'),
    'ProbDetOI_LastVst': ('treatment', 'probDetectOISinceLastVisit'),
    'ProbSwitchSecProph': ('treatment', 'probSwitchSecondaryProph'),
}


def get_param_metadata():
    """Get metadata about parameters for UI generation."""
    return {
        'tabs': [
            {'id': 'runspecs', 'name': 'Run Specs', 'description': 'Run configuration and cohort settings'},
            {'id': 'output', 'name': 'Output', 'description': 'Output and tracing settings'},
            {'id': 'cohort', 'name': 'Cohort', 'description': 'Initial population characteristics'},
            {'id': 'treatment', 'name': 'Treatment', 'description': 'ART start, fail, and stop policies'},
            {'id': 'ltfu', 'name': 'LTFU', 'description': 'Loss to follow-up parameters'},
            {'id': 'heterogeneity', 'name': 'Heterogeneity', 'description': 'Response propensity settings'},
            {'id': 'sti', 'name': 'STI', 'description': 'Structured treatment interruption'},
            {'id': 'prophs', 'name': 'Prophylaxis', 'description': 'OI prophylaxis settings'},
            {'id': 'arts', 'name': 'ARTs', 'description': 'ART regimen parameters'},
            {'id': 'nathist', 'name': 'Natural History', 'description': 'Disease progression and mortality'},
            {'id': 'chrms', 'name': 'CHRMs', 'description': 'Chronic conditions'},
            {'id': 'costs', 'name': 'Costs', 'description': 'Cost parameters'},
            {'id': 'tb', 'name': 'TB', 'description': 'Tuberculosis settings'},
            {'id': 'qol', 'name': 'QOL', 'description': 'Quality of life modifiers'},
            {'id': 'hivtest', 'name': 'HIV Testing', 'description': 'HIV testing and PrEP'},
            {'id': 'peds', 'name': 'Pediatrics', 'description': 'Pediatric model settings'},
            {'id': 'pedsarts', 'name': 'Peds ARTs', 'description': 'Pediatric ART parameters'},
            {'id': 'pedscosts', 'name': 'Peds Costs', 'description': 'Pediatric costs'},
            {'id': 'eid', 'name': 'EID', 'description': 'Early infant diagnosis'},
            {'id': 'adolescent', 'name': 'Adolescent', 'description': 'Adolescent settings'},
            {'id': 'adolescentarts', 'name': 'Adolescent ARTs', 'description': 'Adolescent ART parameters'},
        ],
        'constants': CONSTANTS,
    }
