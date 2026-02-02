"""
CEPAC Input File Generator - Complete Version

Generates .in files with all keywords expected by SimContext.cpp.
"""

# Constants matching SimContext.h/cpp
# Exact strings from SimContext.cpp in INDEX order (0 to N-1)
CD4_STRATA_STRS = ['CD4vlo', 'CD4_lo', 'CD4mlo', 'CD4mhi', 'CD4_hi', 'CD4vhi']
HVL_STRATA_STRS = ['HVLvlo', 'HVL_lo', 'HVLmlo', 'HVLmed', 'HVLmhi', 'HVL_hi', 'HVLvhi']
# Reversed for SimContext iteration (high index to low)
CD4_STRATA_REV = list(reversed(CD4_STRATA_STRS))  # CD4vhi first
HVL_STRATA_REV = list(reversed(HVL_STRATA_STRS))  # HVLvhi first
TRANSM_RISK_STRS = ['MSM', 'IDU', 'Other']
OI_NUM = 15
ART_NUM_LINES = 10
PROPH_NUM = 3
CHRM_NUM = 10
RISK_FACT_NUM = 5
AGE_YRS = 121
TB_NUM_TESTS = 4
TB_NUM_TREATMENTS = 10
COST_AGE_CAT_NUM = 7
HET_INTV_NUM_PERIODS = 5
RESP_AGE_CAT_NUM = 7
CD4_RESPONSE_NUM = 4
INIT_AGE_NUM_STRATA = 30
TRANSM_RISK_AGE_NUM = 7
ART_NUM_SUBREGIMENS = 5
ART_NUM_TOX_SEVERITY = 3
ART_NUM_TOX_PER_SEVERITY = 3
CD4_NUM_STRATA = 6
HVL_NUM_STRATA = 7
CHRM_AGE_CAT_NUM = 7
CHRM_ORPHANS_AGE_CAT_NUM = 4
CHRM_TIME_PER_NUM = 3
GENDER_NUM = 2


class InputGenerator:
    """Generator for CEPAC .in input files."""

    def __init__(self):
        self.lines = []
        self.p = {}  # Current params

    def generate(self, params):
        """Generate .in file content from parameters dictionary.

        Order matches SimContext::readInputs() exactly:
        1. readRunSpecsInputs, 2. readOutputInputs, 3. readCohortInputs,
        4. readLTFUInputs, 5. readHeterogeneityInputs, 6. readHIVTestInputs,
        7. readNatHistInputs, 8. readCHRMsInputs, 9. readQOLInputs,
        10. readCostInputs, 11. readARTInputs, 12. readProphInputs,
        13. readSTIInputs, 14. readTBInputs, 15. readPedsInputs,
        16. readPedsProphInputs, 17. readPedsARTInputs, 18. readPedsCostInputs,
        19. readEIDInputs, 20. readAdolescentInputs, 21. readAdolescentARTInputs
        """
        self.lines = []
        self.p = params

        # Order matches SimContext::readInputs() exactly
        # 1-3: RunSpecs, Output, Cohort
        self._gen_runspecs()
        self._gen_output()
        self._gen_cohort()
        # 4-6: LTFU, Heterogeneity, HIVTest
        self._gen_ltfu()
        self._gen_heterogeneity()
        self._gen_hivtest()
        # 7-10: NatHist, CHRMs, QOL, Costs
        self._gen_nathist()
        self._gen_chrms()
        self._gen_qol()
        self._gen_costs()
        # 11-13: Treatment Part 1, ARTs, Treatment Part 2
        self._gen_treatment_part1()
        self._gen_arts()
        self._gen_treatment_part2()
        # 14-17: Prophs, STI, TB
        self._gen_prophs()
        self._gen_sti()
        self._gen_tb()
        # 18-21: Peds sections
        self._gen_peds()
        self._gen_peds_prophs()
        self._gen_peds_arts()
        self._gen_peds_costs()
        # 22-24: EID, Adolescent
        self._gen_eid()
        self._gen_adolescent()
        self._gen_adolescent_arts()

        return '\n'.join(self.lines)

    def _w(self, keyword, *values):
        """Write keyword with values."""
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            values = values[0]
        formatted = '\t'.join(self._fmt(v) for v in values)
        self.lines.append(f"{keyword}\t{formatted}")

    def _w2(self, kw1, kw2, *values):
        """Write double-keyword line."""
        if len(values) == 1 and isinstance(values[0], (list, tuple)):
            values = values[0]
        formatted = '\t'.join(self._fmt(v) for v in values)
        self.lines.append(f"{kw1}\t{kw2}\t{formatted}")

    def _fmt(self, v):
        """Format a value for output."""
        if isinstance(v, bool):
            return '1' if v else '0'
        if isinstance(v, float):
            if v == int(v):
                return str(int(v))
            return f"{v:.6g}"
        return str(v)

    def _g(self, section, key, default):
        """Get parameter with default."""
        return self.p.get(section, {}).get(key, default)

    def _gen_runspecs(self):
        """Generate RunSpecs section (readRunSpecsInputs)."""
        p = self.p.get('runspecs', {})
        self._w('Runset', p.get('runSetName', 'DefaultRun'))
        self._w('CohortSize', p.get('numCohorts', 10000))
        self._w('DiscFactor', p.get('discountFactor', 0.03))
        self._w('MaxPatCD4', p.get('maxPatientCD4', 2000.0))
        self._w('MthRecARTEffA', p.get('monthRecordARTEfficacyA', 6))
        self._w('MthRecARTEffB', p.get('monthRecordARTEfficacyB', 12))
        self._w('MthRecARTEffC', p.get('monthRecordARTEfficacyC', 24))
        self._w('RandSeedByTime', p.get('randomSeedByTime', 1))
        self._w('UserLocale', p.get('userProgramLocale', 'en_US'))
        self._w('InpVer', p.get('inputVersion', '20210615'))
        self._w('ModelVer', p.get('modelVersion', '50d'))
        self._w('IncludeTB_AsOI', p.get('OIsIncludeTB', 0))
        self._w('OIstrs', *[f'OI{i+1}' for i in range(OI_NUM)])
        self._w('LongitLogCohort', 0)
        self._w('LongitLogFirstOIs', *([0] * OI_NUM))
        self._w('LogPriorOIHistProb', 0)
        self._w('LogOIHistwithARTfails', 0)
        self._w('LogOIHistwithCD4', 0.0, 2000.0)
        self._w('LogOIHistwithHVL', 0, 6)
        self._w('LogOIHistExcludeOITypes', *([0] * OI_NUM))
        self._w('FOB_OIs', *([1.0] * OI_NUM))
        self._w('Severe_OIs', *([0] * OI_NUM))
        self._w('CD4Bounds', 50.0, 100.0, 200.0, 350.0, 500.0)
        self._w('EnableMultDiscountOutput', 0)
        self._w('DiscountRatesCost', 0.0, 0.03, 0.05, 0.07)
        self._w('DiscountRatesBenefit', 0.0, 0.03, 0.05, 0.07)

    def _gen_output(self):
        """Generate Output section (readOutputInputs)."""
        self._w('NumPatientsToTrace', 0)
        self._w('EnableSubCohorts', 0)
        self._w('SubCohortValues', *([0] * 25))
        self._w('EnableDetailedCosts', 0)

    def _gen_cohort(self):
        """Generate Cohort section (readCohortInputs)."""
        p = self.p.get('cohort', {})
        self._w('InitCD4', p.get('initialCD4Mean', 500.0), p.get('initialCD4StdDev', 200.0))
        self._w('UseSqRtTransform', 1)
        # InitHVL uses CD4 strata in reverse order (high to low index)
        for cd4 in CD4_STRATA_REV:
            self._w('InitHVL')
            # HVL values also in reverse order (HVLvhi first)
            self._w(cd4, *[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
        self._w('InitAge', 360.0, 120.0)
        self._w('InitAgeCustomDist', 0)
        self._w('AgeStratMins', *([0.0] * INIT_AGE_NUM_STRATA))
        self._w('AgeStratMaxes', *([0.0] * INIT_AGE_NUM_STRATA))
        self._w('AgeStratProbs', *([0.0] * INIT_AGE_NUM_STRATA))
        self._w('InitGender', 0.5)
        self._w('ProphNonCompliance', 0.0, 0.0)
        self._w('PatClinicTypes', 0.0, 0.0, 1.0)
        self._w('PatTreatmentTypes', 0.0, 0.0, 1.0)
        self._w('PatCD4ResponeTypeOnART', 0.25, 0.25, 0.25, 0.25)

        # PriorOIHistAtEntry: keyword once, then OI + HVL strata (all in reverse order)
        self._w('PriorOIHistAtEntry')
        for oi in range(OI_NUM):
            self.lines.append(f"OI{oi+1}")
            for hvl in HVL_STRATA_REV:
                self._w(hvl, *([0.0] * CD4_NUM_STRATA))

        self._w('ProbRiskFactorPrev', *([0.0] * RISK_FACT_NUM))
        self._w('ProbRiskFactorIncid', *([0.0] * RISK_FACT_NUM))
        self._w('GenRiskFactorStrs', *[f'Risk{i+1}' for i in range(RISK_FACT_NUM)])
        self._w('ShowTransmissionOutput', 0)

        # TransmissionRate uses HVL strata in reverse order
        for hvl in HVL_STRATA_REV:
            self._w2('TransmissionRateOnART', hvl, *([0.0] * CD4_NUM_STRATA))
        self._w2('TransmissionRateOnART', 'Acute', *([0.0] * CD4_NUM_STRATA))
        for hvl in HVL_STRATA_REV:
            self._w2('TransmissionRateOffART', hvl, *([0.0] * CD4_NUM_STRATA))
        self._w2('TransmissionRateOffART', 'Acute', *([0.0] * CD4_NUM_STRATA))

        self._w('TransmissionUseHIVTestAcuteDef', 0)
        self._w('TransmissionAcuteDuration', 3)
        self._w('IntvlTransmissionRateMultiplier', 12, 24)
        self._w('TransmissionRateMultiplier', 1.0, 1.0, 1.0)

        # TransmissionRiskDistribution uses TRANSM_RISK_STRS
        for risk in TRANSM_RISK_STRS:
            # 7 male + 7 female age bins
            self._w2('TransmissionRiskDistribution', risk, *([0.0] * (TRANSM_RISK_AGE_NUM * 2)))

        self._w('TransmissionRiskMultiplierBounds', 12, 24)
        for i in range(3):
            self._w(f'TransmissionRiskMultiplier_T{i+1}', *([1.0] * len(TRANSM_RISK_STRS)))

        self._w('UseDynamicTransmission', 0)
        self._w('DynamicTransmissionNumTransmissionsHRG', 0.0)
        self._w('DynamicTransmissionPropHRGAttrib', 0.0)
        self._w('DynamicTransmissionNumHIVPosHRG', 0.0)
        self._w('DynamicTransmissionNumHIVNegHRG', 0.0)
        self._w('DynamicTransmissionWarmupSize', 0)
        self._w('DynamicTransmissionKeepPrEPAfterWarmup', 0)
        self._w('DynamicTransmissionUsePrEPDuringWarmup', 0)
        self._w('TransmissionUseEndLifeHVLAdjust', 0)
        self._w('TransmissionEndLifeAdjustCD4Threshold', 0.0)
        self._w('TransmissionEndLifeAdjustARTLineThreshold', 0)

    def _gen_treatment_part1(self):
        """Generate Treatment section part 1 (readTreatmentInputsPart1)."""
        self._w('IntvlClinicVisit', 3)
        self._w('ProbDetOI_Entry', *([0.0] * OI_NUM))
        self._w('ProbDetOI_LastVst', *([0.0] * OI_NUM))
        self._w('ProbSwitchSecProph', *([0.0] * OI_NUM))
        self._w('IntvlCD4Tst_CD4Threshold', 200.0)
        self._w('IntvlCD4Tst_MonthsThreshold', 6, 6)
        self._w('IntvlCD4Tst', 6, 3, 3, 6, 3, 6, 6)
        self._w('IntvlHVLTst', 6, 3, 3, 6, 3, 6, 6)
        self._w('HVLtestErrProb', 0.0, 0.0)
        self._w('CD4testErrSDev', 0.15)
        self._w('CD4testBiasMean', 0.0)
        self._w('CD4testBiasSdev', 0.0)
        self._w('ObsvARTFailTestOnRegClinicVst', 1)
        self._w('ARTInitHVLTestsWOClinicVst', 0)
        self._w('ARTInitCD4TestsWOClinicVst', 0)
        self._w('OIVstAsNotSchedClinicVst', 0)
        self._w('LagToCD4Test', 0)
        self._w('LagToHVLTest', 0)
        self._w('StopCD4MonitoringEnable', 0)
        self._w('StopCD4MonitoringThreshold', 0.0)
        self._w('StopCD4MonitoringMthsPostARTInit', 0)

        self._w2('ARTstart_CD4', 'upp', *([2000.0] * ART_NUM_LINES))
        self._w2('ARTstart_CD4', 'lwr', *([0.0] * ART_NUM_LINES))
        self._w2('ARTstart_HVL', 'upp', *([6] * ART_NUM_LINES))
        self._w2('ARTstart_HVL', 'lwr', *([0] * ART_NUM_LINES))
        self._w2('ARTstart_CD4HVL', 'CD4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('ARTstart_CD4HVL', 'CD4lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('ARTstart_CD4HVL', 'HVLupp', *([-1] * ART_NUM_LINES))
        self._w2('ARTstart_CD4HVL', 'HVLlwr', *([-1] * ART_NUM_LINES))

        for oi in range(OI_NUM):
            self._w2('ARTstart_OIs', f'OI{oi+1}', *([0] * ART_NUM_LINES))
        self._w2('ARTstart_OIs', 'numOIs', *([0] * ART_NUM_LINES))

        self._w2('ARTstart_CD4OI', 'CD4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('ARTstart_CD4OI', 'CD4lwr', *([-1.0] * ART_NUM_LINES))
        for oi in range(OI_NUM):
            self._w2('ARTstart_CD4OI', f'OI{oi+1}', *([0] * ART_NUM_LINES))

        self._w2('ARTstart', 'obsvFailFPSuppression', *([0] * ART_NUM_LINES))
        self._w2('ARTstart', 'minMthNum', *([0] * ART_NUM_LINES))
        self._w2('ARTstart', 'maxMthNum', *([9999] * ART_NUM_LINES))
        self._w2('ARTstart', 'MthsSincePrevRegStop', *([0] * ART_NUM_LINES))

    def _gen_arts(self):
        """Generate ARTs section (readARTInputs)."""
        for art_num in range(1, ART_NUM_LINES + 1):
            self._w(f'ART{art_num}Id', -1)
            self._w(f'ART{art_num}InitCost', 0.0)
            self._w(f'ART{art_num}InitCostAdd', 0.0)
            self._w(f'ART{art_num}MthCost', 0.0)
            self._w(f'ART{art_num}MthCostAdd', 0.0)
            self._w(f'ART{art_num}EffTimeHorizon', 6)
            self._w(f'ART{art_num}ResuppEffTimeHorizon', 6)
            self._w(f'ART{art_num}MthForceFail', 9999)
            self._w(f'ART{art_num}MthStageCD4Eff_Succ', 6, 12)
            for resp in ['Full', 'Partial', 'NonResp', 'ARTEffect']:
                self._w2(f'ART{art_num}CD4EffSlope_Succ', resp, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            self._w(f'ART{art_num}MthStageCD4Eff_Fail', 6)
            for resp in ['Full', 'Partial', 'NonResp', 'ARTEffect']:
                self._w2(f'ART{art_num}CD4EffMult_Fail', resp, 1.0, 1.0)
            self._w(f'ART{art_num}MthCD4SecStdDev', 0.0)
            self._w(f'ART{art_num}CD4EffOffART_Succ', 1.0, 1.0)
            self._w(f'ART{art_num}CD4EffOffART_Fail', 1.0, 1.0)
            self._w2(f'ART{art_num}HVLChgProb', 'Supp', 0.0, 0)
            self._w2(f'ART{art_num}HVLChgProb', 'Fail', 0.0, 0)

            for sub in range(ART_NUM_SUBREGIMENS):
                for sev in range(ART_NUM_TOX_SEVERITY):
                    for tox in range(ART_NUM_TOX_PER_SEVERITY):
                        self._w(f'ART{art_num}Toxicity1.{sub}', f'Tox{sev}_{tox}', 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0, 0)
                self._w2(f'ART{art_num}Toxicity1.{sub}', 'TimeToSwitch', 9999)

            self._w(f'ART{art_num}PropMthCostNonResponders', 1.0)
            self._w(f'ART{art_num}ProbRestartRegimen', 0.0, 0.0, 0.0)
            self._w(f'ART{art_num}MaxResuppAttempts', 0)
            self._w(f'ART{art_num}HetPropRespRegCoeff', 0.0, 0.0)
            self._w(f'ART{art_num}HetPropRespRegCoeffDistribution', 0)
            self._w(f'ART{art_num}HetPropRespRegCoeffUseDuration', 0)
            self._w(f'ART{art_num}HetPropRespRegCoeffDuration', 0.0, 0.0)
            self._w2(f'ART{art_num}HetOutcomes', 'Supp', 0.0, 1.0, 0.0, 1.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'LateFail', 0.0, 1.0, 0.0, 1.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'ARTEffectOI', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'ARTEffectCHRMs', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'ARTEffectMort', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'Resist', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'Tox', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'Cost', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'RestartAfterFail', 0.0, 1.0)
            self._w2(f'ART{art_num}HetOutcomes', 'Resuppression', 0.0, 1.0, 0.0, 1.0, 1.0)
            self._w(f'ART{art_num}ARTEffectOnFail', 0)

    def _gen_treatment_part2(self):
        """Generate Treatment section part 2 (readTreatmentInputsPart2)."""
        self._w('EnableSTIforART', *([0] * ART_NUM_LINES))
        self._w('ARTfail_hvlNumIncr', *([0] * ART_NUM_LINES))
        self._w2('ARTfail_hvlAbsol', 'uppBnd', *([-1] * ART_NUM_LINES))
        self._w2('ARTfail_hvlAbsol', 'lwrBnd', *([-1] * ART_NUM_LINES))
        self._w('ARTfail_hvlAtSetptAsFailDiag', *([0] * ART_NUM_LINES))
        self._w('ARTfail_hvlMthsFromInit', *([0] * ART_NUM_LINES))
        self._w('ARTfail_cd4PercDrop', *([0.0] * ART_NUM_LINES))
        self._w('ARTfail_cd4BelowPreARTNadir', *([0] * ART_NUM_LINES))
        self._w2('ARTfail_cd4AbsolOR', 'uppBnd', *([-1.0] * ART_NUM_LINES))
        self._w2('ARTfail_cd4AbsolOR', 'lwrBnd', *([-1.0] * ART_NUM_LINES))
        self._w2('ARTfail_cd4AbsolAND', 'uppBnd', *([-1.0] * ART_NUM_LINES))
        self._w2('ARTfail_cd4AbsolAND', 'lwrBnd', *([-1.0] * ART_NUM_LINES))
        self._w('ARTfail_cd4MthsFromInit', *([0] * ART_NUM_LINES))

        for oi in range(OI_NUM):
            self._w2('ARTfail_OIs', f'OI{oi+1}', *([0] * ART_NUM_LINES))
        self._w('ARTfail_OIsMinNum', *([0] * ART_NUM_LINES))
        self._w('ARTfail_OIsMthsFromInit', *([0] * ART_NUM_LINES))

        self._w('ARTfail_diagNumTestsFail', *([1] * ART_NUM_LINES))
        self._w('ARTfail_diagUseHVLTestsConfirm', *([0] * ART_NUM_LINES))
        self._w('ARTfail_diagUseCD4TestsConfirm', *([0] * ART_NUM_LINES))
        self._w('ARTfail_diagNumTestsConfirm', *([0] * ART_NUM_LINES))

        self._w('ARTstop_MaxMthsOnART', *([9999] * ART_NUM_LINES))
        self._w('ARTstop_MajorToxicity', *([0] * ART_NUM_LINES))
        self._w('ARTstop_OnFailImmed', *([0] * ART_NUM_LINES))
        self._w('ARTstop_OnFailBelowCD4', *([-1.0] * ART_NUM_LINES))
        self._w('ARTstop_OnFailSevereOI', *([0] * ART_NUM_LINES))
        self._w('ARTstop_OnFailMthsAfterObsv', *([0] * ART_NUM_LINES))
        self._w('ARTstop_OnFailMinMthNum', *([0] * ART_NUM_LINES))
        self._w('ARTstop_OnFailMthsFromInit', *([0] * ART_NUM_LINES))
        self._w('ARTStopMajorToxNextLine', *([-1] * ART_NUM_LINES))

        for i in range(ART_NUM_LINES):
            self._w2('ARTresistRed_initSucc', f'reg_{i+1}', *([0.0] * ART_NUM_LINES))
        self._w('ARTresistRed_HVL', *([0.0] * 7))

        # Primary proph start
        self._w2('PriProphStart', 'boolFlag', *([0] * OI_NUM))
        self._w2('PriProphStart', 'curCD4upp', *([-1.0] * OI_NUM))
        self._w2('PriProphStart', 'curCD4lwr', *([-1.0] * OI_NUM))
        self._w2('PriProphStart', 'minCD4upp', *([-1.0] * OI_NUM))
        self._w2('PriProphStart', 'minCD4lwr', *([-1.0] * OI_NUM))
        for oi in range(OI_NUM):
            self._w2('PriProphStart', f'OI{oi+1}', *([0] * OI_NUM))
        self._w2('PriProphStart', 'minMthNum', *([0] * OI_NUM))

        # Primary proph stop
        self._w2('PriProphStop', 'boolFlag', *([0] * OI_NUM))
        self._w2('PriProphStop', 'curCD4upp', *([-1.0] * OI_NUM))
        self._w2('PriProphStop', 'curCD4lwr', *([-1.0] * OI_NUM))
        self._w2('PriProphStop', 'minCD4upp', *([-1.0] * OI_NUM))
        self._w2('PriProphStop', 'minCD4lwr', *([-1.0] * OI_NUM))
        for oi in range(OI_NUM):
            self._w2('PriProphStop', f'OI{oi+1}', *([0] * OI_NUM))
        self._w2('PriProphStop', 'minMthNum', *([0] * OI_NUM))
        self._w2('PriProphStop', 'mthsOnProph', *([9999] * OI_NUM))

        # Secondary proph start
        self._w2('SecProphStart', 'boolFlag', *([0] * OI_NUM))
        self._w2('SecProphStart', 'curCD4upp', *([-1.0] * OI_NUM))
        self._w2('SecProphStart', 'curCD4lwr', *([-1.0] * OI_NUM))
        self._w2('SecProphStart', 'minCD4upp', *([-1.0] * OI_NUM))
        self._w2('SecProphStart', 'minCD4lwr', *([-1.0] * OI_NUM))
        for oi in range(OI_NUM):
            self._w2('SecProphStart', f'OI{oi+1}', *([0] * OI_NUM))
        self._w2('SecProphStart', 'minMthNum', *([0] * OI_NUM))

        # Secondary proph stop
        self._w2('SecProphStop', 'boolFlag', *([0] * OI_NUM))
        self._w2('SecProphStop', 'curCD4upp', *([-1.0] * OI_NUM))
        self._w2('SecProphStop', 'curCD4lwr', *([-1.0] * OI_NUM))
        self._w2('SecProphStop', 'minCD4upp', *([-1.0] * OI_NUM))
        self._w2('SecProphStop', 'minCD4lwr', *([-1.0] * OI_NUM))
        for oi in range(OI_NUM):
            self._w2('SecProphStop', f'OI{oi+1}', *([0] * OI_NUM))
        self._w2('SecProphStop', 'minMthNum', *([0] * OI_NUM))
        self._w2('SecProphStop', 'mthsOnProph', *([9999] * OI_NUM))

    def _gen_ltfu(self):
        """Generate LTFU section (readLTFUInputs)."""
        self._w('UseLTFU', 0)
        self._w('PropRespLTFUPreART', 0.0, 0.0)
        self._w('UseInterventionHetOutcomes', 0)
        self._w2('HetOutcomes', 'LTFU', 0.0, 1.0, 0.0, 1.0)
        for i in range(HET_INTV_NUM_PERIODS):
            self._w2(f'HetOutcomesPeriod{i}', 'LTFU', 0.0, 1.0, 0.0, 1.0)
        self._w2('HetOutcomesOffIntervention', 'LTFU', 0.0, 1.0, 0.0, 1.0)
        self._w('PropGenMedCostsByState', 1.0, 1.0, 1.0, 1.0)
        self._w('PropInterventionCostsByState', 1.0, 1.0, 1.0, 1.0)
        self._w('pLTFUOIProph', 1.0)
        self._w('pLTFUOITreat', 1.0)
        self._w('RTCMinMonthsLost', 0)
        self._w('RTCBackground', 0.0)
        self._w('RTCCD4', 0.0)
        self._w('RTCAcuteSevereOI', 0.0)
        self._w('RTCAcuteMildOI', 0.0)
        self._w('RTCTBPosDiagnosis', 0.0)
        self._w('RTCCD4Threshold', 0.0)
        self._w('RTCSevereOIType', *([0] * OI_NUM))
        self._w('RTCMaxTimePrevOnART', 9999)
        self._w('RTCProbTakeSameART', 0.0)
        self._w('RTCRecheckARTPolicies', 0)
        self._w('RTCProbSuppByPrevOutcome', 0)
        self._w('RTCProbSuppPrevFail', *([0.0] * ART_NUM_LINES))
        self._w('RTCProbSuppPrevSupp', *([0.0] * ART_NUM_LINES))
        self._w('RTCProbResumeIntervention', 0.0)
        self._w('RTCResumeInterventionCost', 0.0)

    def _gen_heterogeneity(self):
        """Generate Heterogeneity section (readHeterogeneityInputs)."""
        self._w('PropRespBaseline', 0.0, 0.0)
        self._w('PropRespAge', *([0.0] * RESP_AGE_CAT_NUM))
        self._w('PropRespPedsAge', 0.0, 0.0)
        self._w('PropRespCD4', *([0.0] * 6))
        self._w('PropRespFemale', 0.0)
        self._w('PropRespHistOIs', 0.0)
        self._w('PropRespPriorARTTox', 0.0)
        self._w('PropRespRiskFactors', *([0.0] * RISK_FACT_NUM))
        self._w('UseIntervention', *([0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionDurationMean', *([0.0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionDurationSD', *([0.0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionPropAdjustmentMean', *([0.0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionPropAdjustmentSD', *([0.0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionPropAdjustmentDistribution', *([0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionCostStartup', *([0.0] * HET_INTV_NUM_PERIODS))
        self._w('InterventionCostMonthly', *([0.0] * HET_INTV_NUM_PERIODS))

    def _gen_sti(self):
        """Generate STI section (readSTIInputs)."""
        self._w2('STIstart_CD4', 'upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STIstart_CD4', 'lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('STIstart_HVL', 'upp', *([-1] * ART_NUM_LINES))
        self._w2('STIstart_HVL', 'lwr', *([-1] * ART_NUM_LINES))
        self._w2('STIstart_CD4HVL', 'CD4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STIstart_CD4HVL', 'CD4lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('STIstart_CD4HVL', 'HVLupp', *([-1] * ART_NUM_LINES))
        self._w2('STIstart_CD4HVL', 'HVLlwr', *([-1] * ART_NUM_LINES))
        for oi in range(OI_NUM):
            self._w2('STIstart_OIs', f'OI{oi+1}', *([0] * ART_NUM_LINES))
        self._w2('STIstart_OIs', 'numOIs', *([0] * ART_NUM_LINES))
        self._w2('STIstart_CD4OI', 'CD4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STIstart_CD4OI', 'CD4lwr', *([-1.0] * ART_NUM_LINES))
        for oi in range(OI_NUM):
            self._w2('STIstart_CD4OI', f'OI{oi+1}', *([0] * ART_NUM_LINES))
        self._w2('STIstart', 'minMthNum', *([0] * ART_NUM_LINES))
        self._w2('STIstart', 'minMthNum_ARTinit', *([0] * ART_NUM_LINES))

        self._w2('STI_restartART', 'cd4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STI_restartART', 'cd4lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('STI_restartART', 'hvlupp', *([-1] * ART_NUM_LINES))
        self._w2('STI_restartART', 'hvllwr', *([-1] * ART_NUM_LINES))
        self._w2('STI_restopART', 'cd4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STI_restopART', 'cd4lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('STI_restopART', 'hvlupp', *([-1] * ART_NUM_LINES))
        self._w2('STI_restopART', 'hvllwr', *([-1] * ART_NUM_LINES))

        self._w2('STIendpt_CD4', 'upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STIendpt_CD4', 'lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('STIendpt_HVL', 'upp', *([-1] * ART_NUM_LINES))
        self._w2('STIendpt_HVL', 'lwr', *([-1] * ART_NUM_LINES))
        self._w2('STIendpt_CD4HVL', 'CD4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STIendpt_CD4HVL', 'CD4lwr', *([-1.0] * ART_NUM_LINES))
        self._w2('STIendpt_CD4HVL', 'HVLupp', *([-1] * ART_NUM_LINES))
        self._w2('STIendpt_CD4HVL', 'HVLlwr', *([-1] * ART_NUM_LINES))
        for oi in range(OI_NUM):
            self._w2('STIendpt_OIs', f'OI{oi+1}', *([0] * ART_NUM_LINES))
        self._w2('STIendpt_OIs', 'numOIs', *([0] * ART_NUM_LINES))
        self._w2('STIendpt_CD4OI', 'CD4upp', *([-1.0] * ART_NUM_LINES))
        self._w2('STIendpt_CD4OI', 'CD4lwr', *([-1.0] * ART_NUM_LINES))
        for oi in range(OI_NUM):
            self._w2('STIendpt_CD4OI', f'OI{oi+1}', *([0] * ART_NUM_LINES))
        self._w2('STIendpt', 'minMthNum', *([9999] * ART_NUM_LINES))

    def _gen_prophs(self):
        """Generate Prophs section (readProphInputs)."""
        for oi in range(OI_NUM):
            for proph in range(PROPH_NUM):
                base = f'OI{oi+1}_PriProph{proph+1}'
                self._w2(base, 'Id', -1)
                self._w2(base, 'EffPriOIs', *([0.0] * OI_NUM))
                self._w2(base, 'EffSecOIs', *([0.0] * OI_NUM))
                self._w2(base, 'Resist', 0.0, 0.0, 0, 0.0, 1.0)
                self._w2(base, 'Tox', 0.0, 0.0, 0, 1.0)
                self._w2(base, 'CostQOL', 0.0, 0.0, 0.0, 0.0, 0.0)
                self._w2(base, 'Switch', 9999, 0, 0)

        for oi in range(OI_NUM):
            for proph in range(PROPH_NUM):
                base = f'OI{oi+1}_SecProph{proph+1}'
                self._w2(base, 'Id', -1)
                self._w2(base, 'EffPriOIs', *([0.0] * OI_NUM))
                self._w2(base, 'EffSecOIs', *([0.0] * OI_NUM))
                self._w2(base, 'Resist', 0.0, 0.0, 0.0, 0.0, 1.0)
                self._w2(base, 'Tox', 0.0, 0.0, 0, 1.0)
                self._w2(base, 'CostQOL', 0.0, 0.0, 0.0, 0.0, 0.0)
                self._w2(base, 'Switch', 9999, 0, 0)

    def _gen_nathist(self):
        """Generate NatHist section (readNatHistInputs)."""
        self._w('HIVDthRateRatio', *([1.0] * 6))
        self._w('ARTDthRateRatio', 1.0)
        for cd4 in CD4_STRATA_REV:
            self._w2('OIProb_NoHist_noART', cd4, *([0.0] * OI_NUM))
        for cd4 in CD4_STRATA_REV:
            self._w2('OIProb_Hist_noART', cd4, *([0.0] * OI_NUM))
        for cd4 in CD4_STRATA_REV:
            self._w2('OIProb_onART_Mult', cd4, *([1.0] * OI_NUM))
        self._w('AcuteOIDthRateRatio', *([1.0] * 6))
        self._w('AcuteOIDthRateRatioTB', *([1.0] * 6))
        self._w('SevrOI_HistDthRateRatio', 1.0)
        self._w('SevrOI_HistEffectDuration', 0)
        self._w('TB_OI_HistDthRateRatio', 1.0)
        self._w('TB_OI_HistEffectDuration', 0)
        self._w('GenRiskDthRateRatio', *([1.0] * RISK_FACT_NUM))
        for cd4 in CD4_STRATA_REV:
            self._w2('BslCD4Decl_Mean', cd4, *([0.0] * 7))
            self._w2('BslCD4Decl_SDev', cd4, *([0.0] * 7))
        self._w('BslCD4Decl_BtwSbjct', 0.0)
        self._w('BackgroundDthRate_Male', *([0.0] * AGE_YRS))
        self._w('BackgroundDthRate_Female', *([0.0] * AGE_YRS))
        self._w('BackgroundMortModifierType', 0)
        self._w('BackgroundMortModifier', 1.0)

    def _gen_chrms(self):
        """Generate CHRMs section (readCHRMsInputs)."""
        chrm_gender_age = GENDER_NUM * CHRM_AGE_CAT_NUM  # 2 * 7 = 14 values per line
        self._w('CHRMstrs', *[f'CHRM{i+1}' for i in range(CHRM_NUM)])
        self._w('ShowCHRMOutput', 0)
        self._w('EnableOrphans', 0)
        self._w('ShowOrphansOutput', 0)
        # CHRMAgeCat: CHRM_AGE_CAT_NUM - 1 = 6 age bounds
        for i in range(CHRM_NUM):
            self._w(f'CHRMAgeCatCHRM{i+1}', *([0] * (CHRM_AGE_CAT_NUM - 1)))
        # Duration for stages 0, 1 (CHRM_TIME_PER_NUM - 1 = 2)
        for stage in range(CHRM_TIME_PER_NUM - 1):
            for chrm in range(CHRM_NUM):
                self._w(f'Duration{stage}andSDCHRM{chrm+1}', 0.0, 0.0)
        self._w('CHRMDurationUseSqrtTrans', 0)

        # ProbPrevCHRM: GENDER_NUM × CHRM_AGE_CAT_NUM = 14 values
        for chrm in range(CHRM_NUM):
            self._w2(f'ProbPrevCHRM_CHRM{chrm+1}', 'HIVneg', *([0.0] * chrm_gender_age))
            for cd4 in CD4_STRATA_REV:
                self._w2(f'ProbPrevCHRM_CHRM{chrm+1}', cd4, *([0.0] * chrm_gender_age))
        for chrm in range(CHRM_NUM):
            self._w2('PrevCHRMRiskLogit', f'CHRM{chrm+1}', *([0.0] * RISK_FACT_NUM))
        for chrm in range(CHRM_NUM):
            self._w2('PrevCHRMNumMonths', f'CHRM{chrm+1}', 0.0, 0.0)
        for chrm in range(CHRM_NUM):
            self._w2('PrevCHRMNumMonthsOrphans', f'CHRM{chrm+1}', *([0] * CHRM_ORPHANS_AGE_CAT_NUM))

        self._w('MinMthsSincePrevCHRMSOrphans', 0)
        # ProbIncidCHRM: GENDER_NUM × CHRM_AGE_CAT_NUM = 14 values
        for chrm in range(CHRM_NUM):
            self._w2(f'ProbIncidCHRM_CHRM{chrm+1}', 'HIVneg', *([0.0] * chrm_gender_age))
            for cd4 in CD4_STRATA_REV:
                self._w2(f'ProbIncidCHRM_CHRM{chrm+1}', cd4, *([0.0] * chrm_gender_age))
        # IncidCHRMOnARTMult: CD4_NUM_STRATA values
        for chrm in range(CHRM_NUM):
            self._w2('IncidCHRMOnARTMult', f'CHRM{chrm+1}', *([1.0] * CD4_NUM_STRATA))
        for chrm in range(CHRM_NUM):
            self._w2('IncidCHRMRiskLogit', f'CHRM{chrm+1}', *([0.0] * RISK_FACT_NUM))
        for chrm in range(CHRM_NUM):
            self._w2('IncidCHRMHistoryLogit', f'CHRM{chrm+1}', *([0.0] * CHRM_NUM))

        # DthRateRatio, Cost, QOL: CHRM_TIME_PER_NUM = 3 stages, 14 values each
        for chrm in range(CHRM_NUM):
            for t in range(CHRM_TIME_PER_NUM):
                self._w(f'DthRateRatioCHRM_CHRM{chrm+1}_T{t+1}', *([1.0] * chrm_gender_age))
        for chrm in range(CHRM_NUM):
            for t in range(CHRM_TIME_PER_NUM):
                self._w2(f'CostCHRM_CHRM{chrm+1}', f'T{t+1}', *([0.0] * chrm_gender_age))
            self._w(f'CostDeathCHRM_CHRM{chrm+1}', 0.0)
        for chrm in range(CHRM_NUM):
            for t in range(CHRM_TIME_PER_NUM):
                self._w2(f'QOLCHRM_CHRM{chrm+1}', f'T{t+1}', *([0.0] * chrm_gender_age))
            self._w(f'QOLModDeathCHRM_CHRM{chrm+1}', 0.0)
        self._w('QOLModMultipleCHRMs', *([1.0] * (CHRM_NUM - 1)))

    def _gen_costs(self):
        """Generate Costs section (readCostInputs)."""
        self._w2('CostAgeBounds', 'EndYr', *([18, 25, 35, 45, 55, 65]))

        for t in range(1, COST_AGE_CAT_NUM + 1):
            for oi in range(OI_NUM):
                self._w2(f'AgeCat{t}CostAcuteOI_noART_treated', f'OI{oi+1}', *([0.0] * 4))
            for oi in range(OI_NUM):
                self._w2(f'AgeCat{t}CostAcuteOI_noART_untreated', f'OI{oi+1}', *([0.0] * 4))
            for oi in range(OI_NUM):
                self._w2(f'AgeCat{t}CostAcuteOI_onART_treated', f'OI{oi+1}', *([0.0] * 4))
            for oi in range(OI_NUM):
                self._w2(f'AgeCat{t}CostAcuteOI_onART_untreated', f'OI{oi+1}', *([0.0] * 4))
            self._w(f'AgeCat{t}CostCD4Test', *([0.0] * 4))
            self._w(f'AgeCat{t}CostHVLTest', *([0.0] * 4))
            # DTH_NUM_CAUSES_BASIC = 17: OI1-OI15, HIV, backgroundMort
            dth_causes = [f'OI{i+1}' for i in range(OI_NUM)] + ['HIV', 'backgroundMort']
            for cause in dth_causes:
                self._w2(f'AgeCat{t}CostDth_noART_treated', cause, *([0.0] * 4))
            for cause in dth_causes:
                self._w2(f'AgeCat{t}CostDth_noART_untreated', cause, *([0.0] * 4))
            for cause in dth_causes:
                self._w2(f'AgeCat{t}CostDth_onART_treated', cause, *([0.0] * 4))
            for cause in dth_causes:
                self._w2(f'AgeCat{t}CostDth_onART_untreated', cause, *([0.0] * 4))

        self._w('CostGenMed_dmed', *([0.0] * 14))
        self._w('CostGenMed_nmed', *([0.0] * 14))
        self._w('CostGenMed_time', *([0.0] * 14))
        self._w('CostGenMed_indr', *([0.0] * 14))

        for cd4 in CD4_STRATA_REV:
            self._w2('CostRoutine_HIVpos_noART_dmed', cd4, *([0.0] * 14))
            self._w2('CostRoutine_HIVpos_noART_nmed', cd4, *([0.0] * 14))
            self._w2('CostRoutine_HIVpos_noART_time', cd4, *([0.0] * 14))
            self._w2('CostRoutine_HIVpos_noART_indr', cd4, *([0.0] * 14))
        for cd4 in CD4_STRATA_REV:
            self._w2('CostRoutine_HIVpos_onART_dmed', cd4, *([0.0] * 14))
            self._w2('CostRoutine_HIVpos_onART_nmed', cd4, *([0.0] * 14))
            self._w2('CostRoutine_HIVpos_onART_time', cd4, *([0.0] * 14))
            self._w2('CostRoutine_HIVpos_onART_indr', cd4, *([0.0] * 14))

        self._w('CostNeg_dmed', *([0.0] * 14))
        self._w('CostNeg_nmed', *([0.0] * 14))
        self._w('CostNeg_time', *([0.0] * 14))
        self._w('CostNeg_indr', *([0.0] * 14))
        self._w('CostNegStopAge', 999)
        self._w('CostUndet_dmed', *([0.0] * 14))
        self._w('CostUndet_nmed', *([0.0] * 14))
        self._w('CostUndet_time', *([0.0] * 14))
        self._w('CostUndet_indr', *([0.0] * 14))
        self._w('CostUndetStopAge', 999)

        # GENDER_STRS = "male", "female" (lowercase)
        for t in range(1, COST_AGE_CAT_NUM + 1):
            for gender in ['male', 'female']:
                for cd4 in CD4_STRATA_REV:
                    self._w2(f'AgeCat{t}CostVisit_{gender}_routine', cd4, *([0.0] * 4))

    def _gen_tb(self):
        """Generate TB section (readTBInputs)."""
        TB_NUM_STATES_LOCAL = 6
        TB_INFECT_NUM_AGE_CAT = 7
        TB_NUM_STRAINS = 3

        self._w('EnableTB', 0)
        self._w('TBClinicIntegrated', 0)
        self._w2('ProbTB_Entry', 'HIV_Neg', *([0.0] * TB_NUM_STATES_LOCAL))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbTB_Entry', cd4, *([0.0] * TB_NUM_STATES_LOCAL))
        self._w('DistTB_Entry_Strain', *([0.0] * TB_NUM_STRAINS))
        self._w('MthsSinceInitTBTreatStop_Entry', 0.0, 0.0)

        self._w2('ProbSputum_Entry', 'HIV_Neg', *([0.0] * TB_NUM_STATES_LOCAL))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbSputum_Entry', cd4, *([0.0] * TB_NUM_STATES_LOCAL))
        self._w2('ProbImmune_Entry', 'HIV_Neg', *([0.0] * TB_NUM_STATES_LOCAL))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbImmune_Entry', cd4, *([0.0] * TB_NUM_STATES_LOCAL))
        self._w2('ProbSymptoms_Entry', 'HIV_Neg', *([0.0] * TB_NUM_STATES_LOCAL))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbSymptoms_Entry', cd4, *([0.0] * TB_NUM_STATES_LOCAL))

        self._w2('ProbMthTBIncid', 'HIV_Neg', *([0.0] * TB_INFECT_NUM_AGE_CAT))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbMthTBIncid', cd4, *([0.0] * TB_INFECT_NUM_AGE_CAT))
        self._w('TBInfectionMultiplier', *([1.0] * TB_NUM_STATES_LOCAL))
        self._w('ProbImmune_Infection', 0.0, *([0.0] * CD4_NUM_STRATA))
        self._w('TBActivationMthThreshold', 12)
        self._w('TBActivationProbActivate1', 0.0, *([0.0] * CD4_NUM_STRATA))
        self._w('TBActivationProbActivate2', 0.0, *([0.0] * CD4_NUM_STRATA))

        # TB Activation/Relapse parameters
        self._w('TBActivationPropPulm', 0.0, *([0.0] * CD4_NUM_STRATA))
        self._w('ProbSputumHiOnActivation', 0.0, *([0.0] * CD4_NUM_STRATA))
        self._w('TBIncidenceRelapse', 1.0, 1.0, 12, 60)
        self._w('TBRelapseFCD4', *([1.0] * CD4_NUM_STRATA))
        self._w('TBTreatDefaultRelapseMult', 1.0)
        self._w('TBRelapsePropPulm', 0.0, *([0.0] * CD4_NUM_STRATA))
        self._w('ProbSputumHiOnRelapse', 0.0, *([0.0] * CD4_NUM_STRATA))
        self._w('TBRelapseMthUnfavorableOutcome', 6)

        # TB Symptoms Incidence (TB_NUM_STATES = 6 values)
        self._w2('TBSymptomsIncidence', 'HIV_Neg', *([0.0] * 6))
        for cd4 in CD4_STRATA_REV:
            self._w2('TBSymptomsIncidence', cd4, *([0.0] * 6))

        # TB Death Rate Ratios
        self._w2('TBDthRateRatio', 'HIV_Neg', 0.0, 0.0)
        for cd4 in CD4_STRATA_REV:
            self._w2('TBDthRateRatio', cd4, 0.0, 0.0)
        self._w('TBDthRateRatioTxSuccessBounds', 6, 12)
        for t in range(1, 4):
            self._w(f'TBDthRateRatioTxSuccessHIVNeg_T{t}', 1.0)
            self._w(f'TBDthRateRatioTxSuccessHIVPos_T{t}', *([1.0] * CD4_NUM_STRATA))
        self._w('TBDthRateRatioTxFailureBounds', 6, 12)
        for t in range(1, 4):
            self._w(f'TBDthRateRatioTxFailureHIVNeg_T{t}', 1.0)
            self._w(f'TBDthRateRatioTxFailureHIVPos_T{t}', *([1.0] * CD4_NUM_STRATA))

        # Natural history multipliers
        self._w('NatHistMultType', 0)
        self._w('NatHistInfectionMult', *([1.0] * 12))
        self._w('NatHistActivationMult', *([1.0] * 12))
        self._w('NatHistReactivationMult', *([1.0] * 12))
        self._w('NatHistRelapseMult', *([1.0] * 12))
        self._w('NatHistMortalityMult', *([1.0] * 12))
        self._w('NatHistMultTimeBounds', 0, 0)
        self._w('NatHistMultTime', 1.0, 1.0, 1.0)
        self._w('TBSelfCureEnable', 0)
        self._w('TBMonthOfSelfCure', 12)

        # TB Prophylaxis policy section
        TB_NUM_PROPHS = 5
        TB_NUM_STATES = 6
        TB_RTC_TIME_CAT_NUM = 5
        COST_NUM_TYPES = 4
        PEDS_COST_AGE_CAT_NUM = 4

        self._w('TBProphOrder', *([0] * TB_NUM_PROPHS))
        self._w('TBProphDuration', *([0] * TB_NUM_PROPHS))
        self._w('TBProphMaxRestarts', *([0] * TB_NUM_PROPHS))

        # TBProphStartKnownPos: useOr, all, CD4UpperBound, CD4LowerBound, ARTStatus, histTBDiag, histTreatment, immuneReactive
        self._w('TBProphStartKnownPos', 0, 0, 9999.0, 0.0, 0, 0, 0, 0)
        # TBProphStartNotKnownPos: useOr, all, histTBDiag, histTreatment, immuneReactive
        self._w('TBProphStartNotKnownPos', 0, 0, 0, 0, 0)
        # TBProphStartPropToReceiveUponQual: probNotKnownPos, probKnownPosOffART, probOnART
        self._w('TBProphStartPropToReceiveUponQual', 0.0, 0.0, 0.0)
        # TBProphStartLagToStart: mean, stddev
        self._w('TBProphStartLagToStart', 0.0, 0.0)
        self._w('TBProphStopMthDropoutProb', 0.0)
        # TBProphStopKnownPos: useOr, CD4UpperBound, CD4LowerBound, numMonths, afterTBDiag, majorTox
        self._w('TBProphStopKnownPos', 0, 9999.0, 0.0, 0, 0, 0)
        # TBProphStopNotKnownPos: useOr, numMonths, afterTBDiag, majorTox
        self._w('TBProphStopNotKnownPos', 0, 0, 0, 0)
        self._w('TBProphMoveToNextAfterTox', 0)

        # Per-prophylaxis efficacy and cost (5 prophylaxis regimens)
        for proph_num in range(TB_NUM_PROPHS):
            # OnTBProph{n}EffInfect: HIVNeg + 6 CD4 strata (VHI to VLO)
            self._w(f'OnTBProph{proph_num}EffInfect', 0.0, *([0.0] * CD4_NUM_STRATA))
            # PostTBProph{n}EffInfect: HIVNeg + 6 CD4 strata + monthsOfEfficacy + decayPeriod
            self._w(f'PostTBProph{proph_num}EffInfect', 0.0, *([0.0] * CD4_NUM_STRATA), 0, 0)

            # OnTBProph{n}EffActivate for DS, MDR, XDR
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'OnTBProph{proph_num}EffActivate', strain, 0.0, *([0.0] * CD4_NUM_STRATA))
            # PostTBProph{n}EffActivate for DS, MDR, XDR with months and decay
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'PostTBProph{proph_num}EffActivate', strain, 0.0, *([0.0] * CD4_NUM_STRATA), 0, 0)

            # OnTBProph{n}EffReinfect for DS, MDR, XDR
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'OnTBProph{proph_num}EffReinfect', strain, 0.0, *([0.0] * CD4_NUM_STRATA))
            # PostTBProph{n}EffReinfect for DS, MDR, XDR with months and decay
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'PostTBProph{proph_num}EffReinfect', strain, 0.0, *([0.0] * CD4_NUM_STRATA), 0, 0)

            # TBProph{n}CostQOL: costMonthly, costMinorTox, QOLMinorTox, costMajorTox, QOLMajorTox
            self._w(f'TBProph{proph_num}CostQOL', 0.0, 0.0, 0.0, 0.0, 0.0)
            # TBProph{n}Toxicity/Minor: probHIVNeg, probOffART, probOnART
            self._w2(f'TBProph{proph_num}Toxicity', 'Minor', 0.0, 0.0, 0.0)
            # TBProph{n}Toxicity/Major: probHIVNeg, probOffART, probOnART, deathRateRatio
            self._w2(f'TBProph{proph_num}Toxicity', 'Major', 0.0, 0.0, 0.0, 1.0)
            self._w(f'TBProph{proph_num}ProbResist', 0.0)

        # TB LTFU section
        self._w('UseTBLTFU', 0)
        self._w('MthsToLongTermEffects', 0)
        self._w('TBMaxMthsLTFU', 0)
        self._w('TBProbLTFU_Stage1', *([0.0] * TB_NUM_STATES))
        self._w('TBProbLTFU_Stage2', *([0.0] * TB_NUM_STATES))
        self._w('TBProbRTCHIVNeg', *([0.0] * TB_NUM_STATES))
        self._w('TBProbRTCHIVPos', *([0.0] * TB_NUM_STATES))
        self._w('TBProphStartWhileHIVLTFU', 0)
        self._w('TBProphStopWhileHIVLTFUProb', 0.0)
        self._w('TBRTCRestartReg', *([0.0] * TB_RTC_TIME_CAT_NUM))
        self._w('TBRTCResumeReg', *([0.0] * TB_RTC_TIME_CAT_NUM))
        self._w('TBRTCRetest', *([0.0] * TB_RTC_TIME_CAT_NUM))
        self._w('TBRTCNextReg', *([0.0] * TB_RTC_TIME_CAT_NUM))

        # TB Costs
        self._w('CostsTBUntreated', *([0.0] * COST_NUM_TYPES))
        self._w2('CostsTBTreated', 'Visit', *([0.0] * COST_NUM_TYPES), 1)  # + frequency
        self._w2('CostsTBTreated', 'Medication', *([0.0] * COST_NUM_TYPES), 1)  # + frequency
        self._w2('CostsTBDeath', 'Adult', *([0.0] * COST_NUM_TYPES))
        for peds_cat in range(1, PEDS_COST_AGE_CAT_NUM + 1):
            self._w(f'Peds{peds_cat}CostsTBDeath', *([0.0] * COST_NUM_TYPES))
        self._w('QOLActiveTB', 0.0)
        self._w('QOLDeathActiveTB', 0.0)

        # TB Diagnostics section
        TB_DIAG_INIT_POLICY_NUM = 6
        TB_DIAG_INIT_POLICY_INTV_NUM = 4
        TB_DIAG_TEST_ORDER_NUM = 4
        TB_DIAG_STATUS_NUM = 2

        self._w('EnableTBDiagnostics', 0)
        self._w('AllowMultipleTestsSameMonth', 0)
        self._w('TBDiagInitPolicyAndOr', 0)
        self._w('TBDiagInitPolicy', *([0] * TB_DIAG_INIT_POLICY_NUM))
        self._w('TBDiagInitPolicySymptomsProb', 0.0)
        self._w('TBDiagInitPolicyCD4Bounds', 9999.0, 0.0)
        self._w('TBDiagInitPolicyCalendarMth', 0)
        self._w('TBDiagInitPolicyMthIntvlProb', 0.0)
        self._w('TBDiagInitPolicyMthIntvlBounds', *([0] * (TB_DIAG_INIT_POLICY_INTV_NUM - 1)))
        self._w('TBDiagInitPolicyMthIntvl', *([0] * TB_DIAG_INIT_POLICY_INTV_NUM))
        self._w('TBDiagInitMinMthsPostTreatment', 0)
        self._w('TBDiagTestOrderNeverTreat', *([0] * TB_DIAG_TEST_ORDER_NUM))
        self._w('TBDiagTestOrderNeverTreatDST', *([0] * TB_DIAG_TEST_ORDER_NUM))
        self._w('TBDiagTestOrderEverTreat', *([0] * TB_DIAG_TEST_ORDER_NUM))
        self._w('TBDiagTestOrderEverTreatDST', *([0] * TB_DIAG_TEST_ORDER_NUM))
        self._w2('TBDiagStartInTreat', 'HIVNeg', *([0.0] * TB_NUM_STATES))
        self._w2('TBDiagStartInTreat', 'HIVPos', *([0.0] * TB_NUM_STATES))
        # TBDiagSeq matrices
        self._w2('TBDiagSeq', '2Tests', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagSeq', '3Tests1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagSeq', '3Tests1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagSeq', '4Tests2Pos1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagSeq', '4Tests2Pos1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagSeq', '4Tests2Neg1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagSeq', '4Tests2Neg1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w('TBDiagAllowIncomplete', 0)
        self._w('TBDiagAllowNoDiagnosis', 0)
        # TBDiagResultMatrix
        self._w2('TBDiagResultMatrix', '1Test', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '2Tests1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '2Tests1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '3Tests2Pos1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '3Tests2Pos1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '3Tests2Neg1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '3Tests2Neg1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Pos2Pos1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Pos2Pos1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Pos2Neg1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Pos2Neg1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Neg2Pos1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Neg2Pos1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Neg2Neg1Pos', *([0] * TB_DIAG_STATUS_NUM))
        self._w2('TBDiagResultMatrix', '4Tests3Neg2Neg1Neg', *([0] * TB_DIAG_STATUS_NUM))
        self._w('TBDiagProbLinkTBTreatmentIntegrated', 1.0)
        self._w('TBDiagProbLinkTBTreatmentUnintegrated', 1.0)
        self._w('TBDiagRTCForHIVUponLinkageIntegrated', 0)
        self._w('TBDiagProbHIVDetUponTBLinkageIntegrated', 0.0)
        self._w('TBDiagProbHIVDetUponTBLinkageUnintegrated', 0.0)

        # TB Tests (4 tests, TB_NUM_TESTS = 4)
        for test_num in range(TB_NUM_TESTS):
            self._w2(f'TBTest{test_num}PosProb', 'HIV_Neg', *([0.0] * TB_NUM_STATES))
            for cd4 in CD4_STRATA_REV:
                self._w2(f'TBTest{test_num}PosProb', cd4, *([0.0] * TB_NUM_STATES))
            self._w(f'TBTest{test_num}ProbAccept', 1.0)
            self._w(f'TBTest{test_num}ProbPickup', 1.0)
            self._w(f'TBTest{test_num}LagToReset', 0)
            self._w(f'TBTest{test_num}MonthsToPickup', 0.0, 0.0)
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'TBTest{test_num}DSTPosProb', strain, *([0.0] * 3), 0)
            self._w(f'TBTest{test_num}DSTLinked', 0)
            self._w(f'TBTest{test_num}DSTProbPickup', 1.0)
            self._w(f'TBTest{test_num}ProbEmpiricWaitingResultsHIVNegSymptomatic', 0.0)
            self._w(f'TBTest{test_num}ProbEmpiricWaitingResultsHIVPosSymptomatic', *([0.0] * CD4_NUM_STRATA))
            self._w(f'TBTest{test_num}ProbEmpiricWaitingResultsHIVNegAsymptomatic', 0.0)
            self._w(f'TBTest{test_num}ProbEmpiricWaitingResultsHIVPosAsymptomatic', *([0.0] * CD4_NUM_STRATA))
            self._w(f'TBTest{test_num}ProbEmpiricPositiveResultHIVNegSymptomatic', 0.0)
            self._w(f'TBTest{test_num}ProbEmpiricPositiveResultHIVPosSymptomatic', *([0.0] * CD4_NUM_STRATA))
            self._w(f'TBTest{test_num}ProbEmpiricPositiveResultHIVNegAsymptomatic', 0.0)
            self._w(f'TBTest{test_num}ProbEmpiricPositiveResultHIVPosAsymptomatic', *([0.0] * CD4_NUM_STRATA))
            self._w(f'TBTest{test_num}ProbEmpiricTestOfferHIVNegSymptomatic', 0.0)
            self._w(f'TBTest{test_num}ProbEmpiricTestOfferHIVPosSymptomatic', *([0.0] * CD4_NUM_STRATA))
            self._w(f'TBTest{test_num}ProbEmpiricTestOfferHIVNegAsymptomatic', 0.0)
            self._w(f'TBTest{test_num}ProbEmpiricTestOfferHIVPosAsymptomatic', *([0.0] * CD4_NUM_STRATA))
            self._w(f'TBTest{test_num}ProbStopEmpiric', 0.0, 0.0)
            self._w(f'TBTest{test_num}InitialCost', 0.0)
            self._w(f'TBTest{test_num}QOLMod', 0.0)
            self._w(f'TBTest{test_num}CostDST', 0.0)

        # TB Treatments
        for strain in ['DS', 'MDR', 'XDR']:
            self._w2('TBTreatProbInitialNeverTreat', strain, *([0.0] * TB_NUM_TREATMENTS))
        for strain in ['DS', 'MDR', 'XDR']:
            self._w2('TBTreatProbInitialEverTreat', strain, *([0.0] * TB_NUM_TREATMENTS))
        self._w('TBTreatProbRepeatLine', *([0.0] * TB_NUM_TREATMENTS))
        self._w('TBTreatNumRepeats', *([0] * TB_NUM_TREATMENTS))
        self._w('TBTreatProbResistAfterFail', *([0.0] * TB_NUM_TREATMENTS))
        self._w('TBTreatProbResistAfterDefault', *([0.0] * TB_NUM_TREATMENTS))
        self._w('TBTreatProbEmpiricMDR', 0.0)
        self._w('TBTreatProbEmpiricXDR', 0.0)
        self._w('TBTreatEmpiricNum', *([0] * 3))

        for treat_num in range(TB_NUM_TREATMENTS):
            self._w(f'TBTreat{treat_num}Stage1Duration', 0)
            self._w(f'TBTreat{treat_num}Stage2Duration', 0)
            self._w(f'TBTreat{treat_num}Cost', 0.0, 0.0, 0.0)
            self._w2(f'TBTreat{treat_num}ProbSuccess', 'HIV_Neg', *([0.0] * 3))
            for cd4 in CD4_STRATA_REV:
                self._w2(f'TBTreat{treat_num}ProbSuccess', cd4, *([0.0] * 3))
            self._w(f'TBTreat{treat_num}ToxProbHIVNeg', 0.0, 0.0, 0.0, 0.0)
            self._w(f'TBTreat{treat_num}ToxProbHIVPos_offART', 0.0, 0.0, 0.0, 0.0)
            self._w(f'TBTreat{treat_num}ToxProbHIVPos_onART', 0.0, 0.0, 0.0, 0.0)
            self._w(f'TBTreat{treat_num}DthRateRatioMajTox', 1.0)
            self._w(f'TBTreat{treat_num}ToxCostHIVNeg', 0.0, 0.0, 0.0, 0.0)
            self._w(f'TBTreat{treat_num}ToxCostHIVPos', 0.0, 0.0, 0.0, 0.0)
            self._w(f'TBTreat{treat_num}ProbObsvEarlyFail', 0.0)
            self._w(f'TBTreat{treat_num}ProbEarlyFailObsvWithTBTest', 0.0)
            self._w(f'TBTreat{treat_num}ObsvFailTBTestCost', 0.0)
            self._w(f'TBTreat{treat_num}ProbSwitchOnObsvEarlyFail', 0.0)
            self._w(f'TBTreat{treat_num}NextTreatNumOnObsvEarlyFail', -1)
            self._w(f'TBTreat{treat_num}NextTreatNumOnRegularFail', -1)
            self._w(f'TBTreat{treat_num}EffInfect', 0.0, *([0.0] * CD4_NUM_STRATA), 0)
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'TBTreat{treat_num}EffActivate', strain, 0.0, *([0.0] * CD4_NUM_STRATA), 0)
            for strain in ['DS', 'MDR', 'XDR']:
                self._w2(f'TBTreat{treat_num}EffReinfect', strain, 0.0, *([0.0] * CD4_NUM_STRATA), 0)
            self._w(f'TBTreat{treat_num}RelapseMult', 1.0)
            self._w(f'TBTreat{treat_num}RelapseMultDuration', 0)

    def _gen_qol(self):
        """Generate QOL section (readQOLInputs)."""
        # HIST_OI_CATS_STRS: NoOIHist, MildOIHist (skipped), SevrOIHist
        for hist in ['NoOIHist', 'SevrOIHist']:
            self._w2('QOLRoutine', hist, *([1.0] * CD4_NUM_STRATA))
        self._w('QOLRoutineOIHistEffectDuration', *([0] * CD4_NUM_STRATA))
        self._w('QOLAcuteOI', *([0.0] * OI_NUM))
        self._w('QOLDeath', 0.0, 0.0, 0.0)
        self._w('QOLBackgroundMale', *([1.0] * AGE_YRS))
        self._w('QOLBackgroundFemale', *([1.0] * AGE_YRS))
        self._w('QOLCalculationType', 0)

    def _gen_hivtest(self):
        """Generate HIVTest section (readHIVTestInputs)."""
        self._w('EnableHIVtest', 0)
        self._w('HIVtestAvail', 0)
        self._w('PrEPEnable', 0)
        self._w('CD4testAvail', 0)
        self._w('AltStopRuleEnable', 0)
        self._w('AltStopRuleTotHIV', 0)
        self._w('AltStopRuleTotCohort', 0)
        self._w2('IncidenceAgeBins', 'EndYr', *([0] * 10))
        self._w('HIVdistNeg', 1.0)
        self._w('HIVdistPosAcute', 0.0)
        self._w('HIVdistPosChr', 0.0)
        self._w('HIVNegRiskDist', 0.5, 0.5)
        self._w('HIVacuteCD4dist', 500.0, 200.0)
        self._w('HIVacuteHVLdist', *([0.0] * 7))
        self._w2('HIVmthIncidMale', 'hiRisk', *([0.0] * 10))
        self._w2('HIVmthIncidMale', 'loRisk', *([0.0] * 10))
        self._w2('HIVmthIncidFemale', 'hiRisk', *([0.0] * 10))
        self._w2('HIVmthIncidFemale', 'loRisk', *([0.0] * 10))
        self._w('UseHIVIncidReductionMult', 0)
        self._w('HIVIncidReductionMult', *([1.0] * 3))
        self._w('HIVIncidReductionMultBounds', *([0] * 2))
        self._w('MthsAcuteToChrHIV', 3)
        self._w('MeanCD4ChgAtChrHIVTrans', *([0.0] * 7))
        self._w('SDevCD4ChgAtChrHIVTrans', *([0.0] * 7))
        for hvl in HVL_STRATA_REV:
            self._w2('HVLDistribAtChrHIVTrans', hvl, *([0.0] * 7))
        self._w('HIVdetectAcute', 0.0)
        self._w('HIVdetectAsympChr', 0.0)
        self._w('HIVdetectSympChr', 0.0)
        self._w('HIVProbDetAtOI', *([0.0] * OI_NUM))
        self._w('HIVProbLinkAtOIDet', *([1.0] * OI_NUM))
        self._w('HIVundetCD4Cost', *([0.0] * 6))
        self._w('HIVundetCD4QOL', *([1.0] * 6))
        self._w('HIVnegDthCost', 0.0)
        self._w('HIVundetHIVDthCost', 0.0)
        self._w('HIVundetBgMortDthCost', 0.0)
        self._w('HIVnegDthQOL', 0.0)
        self._w('HIVundetHIVDthQOL', 0.0)
        self._w('HIVundetBgMortDthQOL', 0.0)
        self._w('HIVtestStartAge', 0)
        self._w('HIVtestStopAge', 999)
        self._w('HIVtestFreqInterval', *([0] * 6))
        self._w('HIVtestFreqProb', *([0.0] * 6))
        for i in range(1, 7):
            self._w(f'HIVtestAcceptDist{i}', *([0.0] * 5))
        for i in range(1, 7):
            self._w(f'HIVtestAcceptProb{i}', *([1.0] * 5))
        self._w('HIVtestRetProb', *([1.0] * 4))
        self._w('HIVtestPosProb', 0.0, 1.0, 1.0, 1.0)
        self._w('HIVtestPosCost', *([0.0] * 4))
        self._w('HIVtestNegCost', *([0.0] * 4))
        self._w('HIVtestPosQOLMod', *([0.0] * 4))
        self._w('HIVtestNegQOLMod', *([0.0] * 4))
        self._w('HIVtestCost', *([0.0] * 4))
        self._w('HIVtestStartupCost', *([0.0] * 5))
        self._w('HIVtestNonRetCost', *([0.0] * 5))
        self._w('HIVtestBgAcceptProb', *([0.0] * 5))
        self._w('HIVtestBgReturnProb', *([1.0] * 5))
        self._w('HIVtestBgPosProb', 0.0, 0.0, 1.0, 1.0, 1.0)
        self._w('HIVtestBgTestCost', *([0.0] * 5))
        self._w('HIVtestBgTestPosCost', *([0.0] * 5))
        self._w('HIVtestBgTestNegCost', *([0.0] * 5))
        self._w('HIVtestBgStartAge', 0)
        self._w('HIVtestBgProbLink', 1.0)
        self._w('HIVtestDetectCost', *([0.0] * 3))
        self._w('PrEPDropoutThreshold', 12)
        self._w('DropoutThresholdRefPrEPStart', 0)
        self._w('PrEPHIVtestAcceptProb', *([1.0] * 2))
        self._w('PrEPInitDist', *([0.0] * 2))
        self._w('PrEPJoinAfterRollout', *([0] * 2))
        self._w('PrEPDropoutPreThreshold', *([0.0] * 2))
        self._w('PrEPDropoutPostThreshold', *([0.0] * 2))
        self._w('PrEPCoverage', *([0.0] * 2))
        self._w('PrEPDuration', *([0] * 2))
        self._w('PrEPShape', *([1.0] * 2))
        self._w('PrEPStartupCost', *([0.0] * 2))
        self._w('PrEPMonthlyCost', *([0.0] * 2))
        self._w('PrEPQoLMod', *([0.0] * 2))
        self._w2('PrepIncidMale', 'hiRisk', *([0.0] * 10))
        self._w2('PrepIncidMale', 'loRisk', *([0.0] * 10))
        self._w2('PrepIncidFemale', 'hiRisk', *([0.0] * 10))
        self._w2('PrepIncidFemale', 'loRisk', *([0.0] * 10))
        self._w('CD4TestAcceptProb', *([1.0] * 3))
        self._w('CD4TestRetProb', *([1.0] * 3))
        self._w('CD4TestStartupCost', *([0.0] * 3))
        self._w('CD4TestCost', *([0.0] * 3))
        self._w('CD4TestNonRetCost', *([0.0] * 3))
        self._w('CD4TestRetCost', *([0.0] * 3))
        self._w('LabStageStdDev', 0.15)
        self._w('LabStageBiasMean', 0.0)
        self._w('LabStageBiasStdDevPerc', 0.0)
        # CD4 linkage probabilities (CD4 strata in reverse order)
        self._w('CD4TestLinkProb', *([1.0] * CD4_NUM_STRATA))

    def _gen_peds(self):
        """Generate Peds section (readPedsInputs)."""
        PEDS_MATERNAL_STATUS_NUM = 4
        PEDS_AGE_INFANT_NUM = 7
        PEDS_AGE_EARLY_NUM = 10
        PEDS_AGE_CHILD_NUM = 11
        PEDS_CD4_PERC_NUM = 8
        PEDS_PP_MATERNAL_ART_STATUS_NUM = 24
        PEDS_EXPOSED_CONDITIONS_NUM = 4
        RISK_FACT_NUM = 5

        PEDS_AGE_CAT_STRS = ["0-2mth", "3-5mth", "6-8mth", "9-11mth", "12-14mth", "15-17mth",
                            "18-23mth", "2yr", "3yr", "4yr", ">4yr"]
        PEDS_CD4_PERC_STRS = ["0-5perc", "5-10perc", "10-15perc", "15-20perc",
                              "20-25perc", "25-30perc", "30-35perc", ">35perc"]
        RISK_FACT_STRS = ["Risk1", "Risk2", "Risk3", "Risk4", "Risk5"]

        self._w('EnablePeds', 0)
        self._w('InitAgePeds', 0.0, 0.0)
        self._w('DistMatStat', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbInfectionMom', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMatMort', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMatStatKnown', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMatStatKnownBF', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMomOnARTPreg', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMomSuppressed', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMomKnownSuppressed', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMomKnownNotSuppressed', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbMomLowHVL', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('DistEarlyVTHIVIU', 0.0)
        self._w2('ProbEarlyVTHIVOnART', 'Suppressed', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbEarlyVTHIVOnART', 'NotSuppressedLowHVL', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbEarlyVTHIVOnART', 'NotSuppressedHighHVL', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('ProbEarlyVTHIVOffART', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbPPVTHIVOnART', 'Suppressed', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbPPVTHIVOnART', 'NotSuppressedLowHVL', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbPPVTHIVOnART', 'NotSuppressedHighHVL', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbPPVTHIVOffART', 'EBF', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbPPVTHIVOffART', 'MBF', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w2('ProbPPVTHIVOffART', 'CBF', *([0.0] * PEDS_MATERNAL_STATUS_NUM))
        self._w('BreastfedDist', 0.0, 0.0)
        self._w('BreastfedStopAge', 0.0, 0.0, 0.0)
        self._w('ProbStopBFWhenVSKnownNotSuppressedLowHVL', 0.0)
        self._w('ProbStopBFWhenVSKnownNotSuppressedHighHVL', 0.0)

        # Initial CD4 percentage
        self._w('InitCD4PercPrevIU', 0.0, 0.0)
        self._w('InitCD4PercPrevIP', 0.0, 0.0)
        for i in range(PEDS_AGE_INFANT_NUM - 1):
            self._w2('InitCD4PercIncidPP', PEDS_AGE_CAT_STRS[i], 0.0, 0.0)
        self._w2('InitCD4PercIncidPP', '18+mth', 0.0, 0.0)

        # Initial HVL
        self._w('InitHVLPrevIU', *([0.0] * HVL_NUM_STRATA))
        self._w('InitHVLPrevIP', *([0.0] * HVL_NUM_STRATA))
        for i in range(PEDS_AGE_INFANT_NUM - 1):
            self._w2('InitHVLIncidPP', PEDS_AGE_CAT_STRS[i], *([0.0] * HVL_NUM_STRATA))
        self._w2('InitHVLIncidPP', '18+mth', *([0.0] * HVL_NUM_STRATA))

        # Adult CD4 strata mapping
        for i in range(PEDS_AGE_EARLY_NUM):
            self._w2('AdultCD4Strata', PEDS_AGE_CAT_STRS[i], *([0] * PEDS_CD4_PERC_NUM))

        # Post-partum maternal ART status
        self._w('UsePPMaternalARTStatus', 0)
        self._w2('PPMaternalARTStatusOnART', 'Suppressed', *([0.0] * PEDS_PP_MATERNAL_ART_STATUS_NUM))
        self._w2('PPMaternalARTStatusOnART', 'NotSuppressedLowHVL', *([0.0] * PEDS_PP_MATERNAL_ART_STATUS_NUM))
        self._w2('PPMaternalARTStatusOnART', 'NotSuppressedHighHVL', *([0.0] * PEDS_PP_MATERNAL_ART_STATUS_NUM))
        self._w('PPMaternalARTStatusOffART', *([0.0] * PEDS_PP_MATERNAL_ART_STATUS_NUM))
        self._w('PPMaternalARTStatusVSKnown', *([0.0] * PEDS_PP_MATERNAL_ART_STATUS_NUM))

        # CD4 percent decline
        for i in range(PEDS_AGE_EARLY_NUM):
            self._w2('CD4PercDeclinePrevIU', PEDS_AGE_CAT_STRS[i], *([0.0] * PEDS_CD4_PERC_NUM))
        for i in range(PEDS_AGE_EARLY_NUM):
            self._w2('CD4PercDeclinePrevIP', PEDS_AGE_CAT_STRS[i], *([0.0] * PEDS_CD4_PERC_NUM))
        for i in range(PEDS_AGE_EARLY_NUM):
            self._w2('CD4PercDeclineIncidPP', PEDS_AGE_CAT_STRS[i], *([0.0] * PEDS_CD4_PERC_NUM))

        # CD4 percent transition to absolute
        for i in range(PEDS_CD4_PERC_NUM):
            self._w2('CD4PercTransition', PEDS_CD4_PERC_STRS[i], 0.0, 0.0)

        # HVL transition
        for hvl in HVL_STRATA_REV:
            self._w2('HVLTransPeds', hvl, *([0.0] * HVL_NUM_STRATA))

        # HIV death rate ratios
        for i in range(PEDS_AGE_EARLY_NUM):
            self._w2('HIVDthRateRatio_PedsEarly', PEDS_AGE_CAT_STRS[i], *([0.0] * PEDS_CD4_PERC_NUM))
        self._w('HIVDthRateRatio_PedsLate', *([0.0] * CD4_NUM_STRATA))

        # Maternal mortality and replacement fed death rate ratios
        self._w('MatMortDeathRateRatioEarly', 1.0, 1.0)
        self._w('MatMortDeathRateRatioDurationEarly', 0)
        self._w('ReplFedDeathRateRatioEarly', 1.0, 1.0)
        self._w('ReplFedDeathRateRatioDurationEarly', 0)
        self._w('MatMortDeathRateRatioLate', 1.0, 1.0)
        self._w('MatMortDeathRateRatioDurationLate', 0)

        # Generic risk death rate ratios
        for risk in RISK_FACT_STRS:
            self._w2('GenRiskDthRateRatio_Peds', risk, *([1.0] * PEDS_AGE_CHILD_NUM))

        # Background death rates
        self._w('BackgroundDthRate_MalePedsEarly', *([0.0] * PEDS_AGE_EARLY_NUM))
        self._w('BackgroundDthRate_FemalePedsEarly', *([0.0] * PEDS_AGE_EARLY_NUM))
        self._w('BackgroundDthRateExposed_MalePedsEarly', *([0.0] * PEDS_AGE_EARLY_NUM))
        self._w('BackgroundDthRateExposed_FemalePedsEarly', *([0.0] * PEDS_AGE_EARLY_NUM))
        self._w('UseExposedDefPeds', 0)
        self._w('ExposedDefEarly', *([0] * PEDS_EXPOSED_CONDITIONS_NUM))

        # Probability of acute OIs
        for oi in range(OI_NUM):
            for j in range(PEDS_AGE_EARLY_NUM):
                self._w2(f'Prob_OI{oi+1}_NoHist', PEDS_AGE_CAT_STRS[j], *([0.0] * PEDS_CD4_PERC_NUM))
            for j in range(PEDS_AGE_EARLY_NUM):
                self._w2(f'Prob_OI{oi+1}_WithHist', PEDS_AGE_CAT_STRS[j], *([0.0] * PEDS_CD4_PERC_NUM))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbOIsNoHistLate', cd4, *([0.0] * OI_NUM))
        for cd4 in CD4_STRATA_REV:
            self._w2('ProbOIsWithHistLate', cd4, *([0.0] * OI_NUM))

        # Acute OI death rate ratios
        for i in range(PEDS_CD4_PERC_NUM):
            self._w2('AcuteOIDthRateRatio_PedsEarly', PEDS_CD4_PERC_STRS[i], *([0.0] * PEDS_AGE_EARLY_NUM))
        for i in range(PEDS_CD4_PERC_NUM):
            self._w2('AcuteOIDthRateRatioTB_PedsEarly', PEDS_CD4_PERC_STRS[i], *([0.0] * PEDS_AGE_EARLY_NUM))
        self._w('SevrOI_HistDthRateRatio_PedsEarly', *([1.0] * PEDS_AGE_EARLY_NUM))
        self._w('SevrOI_HistEffectDuration_PedsEarly', 0)
        self._w('TB_OI_HistDthRateRatio_PedsEarly', *([1.0] * PEDS_AGE_EARLY_NUM))
        self._w('TB_OI_HistEffectDuration_PedsEarly', 0)
        self._w('AcuteOIDthRateRatio_PedsLate', *([0.0] * CD4_NUM_STRATA))
        self._w('AcuteOIDthRateRatioTB_PedsLate', *([0.0] * CD4_NUM_STRATA))
        self._w('SevrOI_HistDthRateRatio_PedsLate', 1.0)
        self._w('SevrOI_HistEffectDuration_PedsLate', 0)
        self._w('TB_OI_HistDthRateRatio_PedsLate', 1.0)
        self._w('TB_OI_HistEffectDuration_PedsLate', 0)

        # ART policies
        self._w('MaxPedsCD4Perc', *([100.0] * PEDS_AGE_EARLY_NUM))
        self._w('IntvlCD4TstPreARTPeds', 3, 3)
        self._w('IntvlHVLTstPreARTPeds', 3, 3)
        self._w('MthStageARTDthRateRatioPeds', 6, 12)
        for t in range(1, 4):
            self._w(f'ARTDthRateRatio_Peds_T{t}', *([1.0] * PEDS_AGE_CHILD_NUM))
        self._w('MthStageRateMultOIsPedsEarly', 6, 12)
        for i in range(PEDS_CD4_PERC_NUM):
            self._w2('RateMultOIsPedsEarly', PEDS_CD4_PERC_STRS[i], 1.0, 1.0, 1.0)
        for cd4 in CD4_STRATA_REV:
            self._w2('RateMultOIsPedsLate', cd4, *([1.0] * OI_NUM))

        # OI names for prophylaxis (must match OIstrs from run specs)
        OI_NAMES = [f'OI{i+1}' for i in range(OI_NUM)]

        # Primary OI prophylaxis starting criteria
        self._w2('PriProphStartPeds', 'agelwr', *([0.0] * OI_NUM))
        self._w2('PriProphStartPeds', 'ageupp', *([999.0] * OI_NUM))
        self._w2('PriProphStartPeds', 'cd4Percupp', *([100.0] * OI_NUM))
        self._w2('PriProphStartPeds', 'cd4Perclwr', *([0.0] * OI_NUM))
        for j in range(OI_NUM):
            self._w2('PriProphStartPeds', OI_NAMES[j], *([0] * OI_NUM))
        self._w('PriProphStartPeds_CondFirst', 0)
        self._w('PriProphStartPeds_CondSecond', 0)
        self._w('PriProphStartPeds_CondPar', 0)

        # Primary OI prophylaxis stopping criteria
        self._w2('PriProphStopPeds', 'agelwr', *([0.0] * OI_NUM))
        self._w2('PriProphStopPeds', 'CD4Perclwr', *([0.0] * OI_NUM))
        for j in range(OI_NUM):
            self._w2('PriProphStopPeds', OI_NAMES[j], *([0] * OI_NUM))
        self._w2('PriProphStopPeds', 'mthsOnProph', *([0] * OI_NUM))
        self._w('PriProphStopPeds_CondFirst', 0)
        self._w('PriProphStopPeds_CondSecond', 0)
        self._w('PriProphStopPeds_CondPar', 0)

        # Secondary OI prophylaxis starting criteria
        self._w2('SecProphStartPeds', 'agelwr', *([0.0] * OI_NUM))
        self._w2('SecProphStartPeds', 'ageupp', *([999.0] * OI_NUM))
        self._w2('SecProphStartPeds', 'cd4Percupp', *([100.0] * OI_NUM))
        self._w2('SecProphStartPeds', 'cd4Perclwr', *([0.0] * OI_NUM))
        for j in range(OI_NUM):
            self._w2('SecProphStartPeds', OI_NAMES[j], *([0] * OI_NUM))
        self._w('SecProphStartPeds_CondFirst', 0)
        self._w('SecProphStartPeds_CondSecond', 0)
        self._w('SecProphStartPeds_CondPar', 0)

        # Secondary OI prophylaxis stopping criteria
        self._w2('SecProphStopPeds', 'agelwr', *([0.0] * OI_NUM))
        self._w2('SecProphStopPeds', 'CD4Perclwr', *([0.0] * OI_NUM))
        for j in range(OI_NUM):
            self._w2('SecProphStopPeds', OI_NAMES[j], *([0] * OI_NUM))
        self._w2('SecProphStopPeds', 'mthsOnProph', *([0] * OI_NUM))
        self._w('SecProphStopPeds_CondFirst', 0)
        self._w('SecProphStopPeds_CondSecond', 0)
        self._w('SecProphStopPeds_CondPar', 0)

        # Peds ART starting criteria
        NUM_ART_START_CD4PERC_PEDS = 4
        self._w('PedsARTstartMthStage', *([0] * (NUM_ART_START_CD4PERC_PEDS - 1)))
        for i in range(NUM_ART_START_CD4PERC_PEDS):
            self._w2(f'PedsARTstart_CD4Perc{i}', 'upp', *([100.0] * ART_NUM_LINES))
            self._w2(f'PedsARTstart_CD4Perc{i}', 'lwr', *([0.0] * ART_NUM_LINES))
        self._w2('PedsARTstart_HVL', 'upp', *([HVL_NUM_STRATA] * ART_NUM_LINES))
        self._w2('PedsARTstart_HVL', 'lwr', *([0] * ART_NUM_LINES))
        for j in range(OI_NUM):
            self._w2('PedsARTstart_OIs', OI_NAMES[j], *([0] * ART_NUM_LINES))
        self._w2('PedsARTstart_OIs', 'numOIs', *([0] * ART_NUM_LINES))
        self._w2('PedsARTstart', 'minMthNum', *([0] * ART_NUM_LINES))
        self._w2('PedsARTstart', 'MthsSincePrevRegStop', *([0] * ART_NUM_LINES))

        # Peds ART failure criteria
        self._w('PedsARTfail_hvlNumIncr', *([0] * ART_NUM_LINES))
        self._w2('PedsARTfail_hvlAbsol', 'uppBnd', *([HVL_NUM_STRATA] * ART_NUM_LINES))
        self._w2('PedsARTfail_hvlAbsol', 'lwrBnd', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_hvlAtSetptAsFailDiag', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_hvlMthsFromInit', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_cd4PercDrop', *([0.0] * ART_NUM_LINES))
        self._w('PedsARTfail_cd4BelowPreARTNadir', *([0] * ART_NUM_LINES))
        self._w2('PedsARTfail_cd4AbsolOR', 'uppBnd', *([100.0] * ART_NUM_LINES))
        self._w2('PedsARTfail_cd4AbsolOR', 'lwrBnd', *([0.0] * ART_NUM_LINES))
        self._w2('PedsARTfail_cd4AbsolAND', 'uppBnd', *([100.0] * ART_NUM_LINES))
        self._w2('PedsARTfail_cd4AbsolAND', 'lwrBnd', *([0.0] * ART_NUM_LINES))
        self._w('PedsARTfail_cd4MthsFromInit', *([0] * ART_NUM_LINES))
        for j in range(OI_NUM):
            self._w2('PedsARTfail_OIs', OI_NAMES[j], *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_OIsMinNum', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_OIsMthsFromInit', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_diagNumTestsFail', *([1] * ART_NUM_LINES))
        self._w('PedsARTfail_diagUseHVLTestsConfirm', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_diagUseCD4TestsConfirm', *([0] * ART_NUM_LINES))
        self._w('PedsARTfail_diagNumTestsConfirm', *([1] * ART_NUM_LINES))

        # Peds ART stopping criteria
        self._w('PedsARTstop_MaxMthsOnART', *([9999] * ART_NUM_LINES))
        self._w('PedsARTstop_MajorToxicity', *([0] * ART_NUM_LINES))
        self._w('PedsARTstop_OnFailImmed', *([0] * ART_NUM_LINES))
        self._w('PedsARTstop_OnFailBelowCD4', *([0.0] * ART_NUM_LINES))
        self._w('PedsARTstop_OnFailSevereOI', *([0] * ART_NUM_LINES))
        self._w('PedsARTstop_OnFailMthsAfterObsv', *([0] * ART_NUM_LINES))
        self._w('PedsARTstop_OnFailMinMthNum', *([0] * ART_NUM_LINES))
        self._w('PedsARTstop_OnFailMthsFromInit', *([0] * ART_NUM_LINES))

    def _gen_peds_prophs(self):
        """Generate PedsProphs section (readPedsProphInputs)."""
        OI_NAMES = [f'OI{i+1}' for i in range(OI_NUM)]
        PROPH_NUM = 3

        # Primary peds prophylaxis for each OI
        for k in range(OI_NUM):
            for i in range(PROPH_NUM):
                prefix = f'OI{k+1}_PriProph{i+1}Peds'
                self._w2(prefix, 'Id', -1)  # NOT_APPL = -1

        # Secondary peds prophylaxis for each OI
        for k in range(OI_NUM):
            for i in range(PROPH_NUM):
                prefix = f'OI{k+1}_SecProph{i+1}Peds'
                self._w2(prefix, 'Id', -1)  # NOT_APPL = -1

    def _gen_peds_arts(self):
        """Generate PedsARTs section (readPedsARTInputs)."""
        # Each peds ART checks for Id == NOT_APPL (-1) and skips if not specified
        for artNum in range(1, ART_NUM_LINES + 1):
            self._w(f'ART{artNum}IdPeds', -1)  # NOT_APPL = -1

    def _gen_peds_costs(self):
        """Generate PedsCosts section (readPedsCostInputs)."""
        PEDS_COST_AGE_CAT_NUM = 4
        COST_NUM_TYPES = 4
        DTH_NUM_CAUSES_BASIC = 17
        OI_NAMES = [f'OI{i+1}' for i in range(OI_NUM)]
        # Death causes: OI1-OI15 (0-14), HIV (15), backgroundMort (16)
        DTH_CAUSES_BASIC = OI_NAMES + ['HIV', 'backgroundMort']

        for t in range(1, PEDS_COST_AGE_CAT_NUM + 1):
            # Acute OI costs
            for oi in OI_NAMES:
                self._w2(f'Peds{t}CostAcuteOI_noART_treated', oi, *([0.0] * COST_NUM_TYPES))
            for oi in OI_NAMES:
                self._w2(f'Peds{t}CostAcuteOI_noART_untreated', oi, *([0.0] * COST_NUM_TYPES))
            for oi in OI_NAMES:
                self._w2(f'Peds{t}CostAcuteOI_onART_treated', oi, *([0.0] * COST_NUM_TYPES))
            for oi in OI_NAMES:
                self._w2(f'Peds{t}CostAcuteOI_onART_untreated', oi, *([0.0] * COST_NUM_TYPES))

            # CD4/HVL test costs
            self._w(f'Peds{t}CostCD4Test', *([0.0] * COST_NUM_TYPES))
            self._w(f'Peds{t}CostHVLTest', *([0.0] * COST_NUM_TYPES))

            # Death costs
            for cause in DTH_CAUSES_BASIC:
                self._w2(f'Peds{t}CostDth_noART_treated', cause, *([0.0] * COST_NUM_TYPES))
            for cause in DTH_CAUSES_BASIC:
                self._w2(f'Peds{t}CostDth_noART_untreated', cause, *([0.0] * COST_NUM_TYPES))
            for cause in DTH_CAUSES_BASIC:
                self._w2(f'Peds{t}CostDth_onART_treated', cause, *([0.0] * COST_NUM_TYPES))
            for cause in DTH_CAUSES_BASIC:
                self._w2(f'Peds{t}CostDth_onART_untreated', cause, *([0.0] * COST_NUM_TYPES))

        # Routine care costs for HIV-neg
        self._w('PedsCostRoutine_HIVneg_dmed', *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
        self._w('PedsCostRoutine_HIVneg_nmed', *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
        self._w('PedsCostRoutine_HIVneg_time', *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
        self._w('PedsCostRoutine_HIVneg_indr', *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))

        # Routine care costs for HIV+ not on ART (by CD4)
        for cd4 in CD4_STRATA_REV:
            self._w2('PedsCostRoutine_HIVpos_noART_dmed', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
            self._w2('PedsCostRoutine_HIVpos_noART_nmed', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
            self._w2('PedsCostRoutine_HIVpos_noART_time', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
            self._w2('PedsCostRoutine_HIVpos_noART_indr', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))

        # Routine care costs for HIV+ on ART (by CD4)
        for cd4 in CD4_STRATA_REV:
            self._w2('PedsCostRoutine_HIVpos_onART_dmed', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
            self._w2('PedsCostRoutine_HIVpos_onART_nmed', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
            self._w2('PedsCostRoutine_HIVpos_onART_time', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))
            self._w2('PedsCostRoutine_HIVpos_onART_indr', cd4, *([0.0] * (GENDER_NUM * PEDS_COST_AGE_CAT_NUM)))

    def _gen_eid(self):
        """Generate EID section (readEIDInputs)."""
        EID_NUM_ASSAYS = 24
        INFANT_HIV_PROPHS_NUM = 4
        INFANT_PROPH_AGES_NUM = 36
        INFANT_PROPH_COST_AGES_NUM = 8
        EID_COST_VISIT_NUM = 24
        EID_NUM_TESTS = 10
        EID_TEST_AGE_CATEGORY_NUM = 18
        PEDS_MATERNAL_STATUS_NUM = 4

        # Enable EID
        self._w('EnableHIVtestEID', 0)
        self._w('AltStopRuleEnableEID', 0)
        self._w('AltStopRuleTotHIVEID', 0)
        self._w('AltStopRuleTotCohortEID', 0)

        # Testing Admin - Unknown Positive
        self._w('EIDTestingAdminAssayUnknownPos', *([0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminAgeUnknownPos', *([0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminProbPresentUnknownPos', *([0.0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminProbNonMaternalUnknownPos', *([0.0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminEIDVisitUnknownPos', *([0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminReofferUnknownPos', *([0] * EID_NUM_ASSAYS))

        # Testing Admin - Known Positive
        self._w('EIDTestingAdminAssayKnownPos', *([0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminAgeKnownPos', *([0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminProbPresentKnownPos', *([0.0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminProbNonMaternalKnownPos', *([0.0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminEIDVisitKnownPos', *([0] * EID_NUM_ASSAYS))
        self._w('EIDTestingAdminReofferKnownPos', *([0] * EID_NUM_ASSAYS))

        # Seroreversion and multipliers
        self._w('EIDAgeSeroreversion', 18, 3)
        self._w('EIDMultProbPresentIfMissedVisit', 1.0)
        self._w('EIDMultProbOfferIfNonMaternal', 1.0)
        self._w('EIDProbKnowledgePriorResult', 1.0)

        # Visit costs
        self._w('EIDCostVisit', *([0.0] * EID_COST_VISIT_NUM))

        # Prob detection on OI
        self._w('EIDProbDetectionOnOI', *([0.0] * OI_NUM))
        self._w('EIDProbOIDetectionConfirmedLabTest', 0.0)
        self._w('EIDOILabTestMonthsThreshold', 0)
        self._w('EIDOIAssayUnknownPos', 0, 0)
        self._w('EIDOIAssayKnownPos', 0, 0)

        # Infant HIV Prophylaxis (4 proph types)
        for prophNum in range(INFANT_HIV_PROPHS_NUM):
            self._w(f'InfantHIVProph{prophNum}Enable', 0)
            self._w(f'InfantHIVProph{prophNum}MaxAge', 0)
            self._w(f'InfantHIVProph{prophNum}MaternalHIVStatusKnown', 0)
            self._w(f'InfantHIVProph{prophNum}MaternalHIVStatusPositive', 0)
            self._w(f'InfantHIVProph{prophNum}MotherOnART', 0)
            self._w(f'InfantHIVProph{prophNum}MaternalVSKnownDelivery', 0)
            self._w(f'InfantHIVProph{prophNum}MotherSuppressedDelivery', 0)
            self._w(f'InfantHIVProph{prophNum}MotherHVLHighDelivery', 0)
            self._w(f'InfantHIVProph{prophNum}MaternalVSKnown', 0)
            self._w(f'InfantHIVProph{prophNum}MotherSuppressed', 0)
            self._w(f'InfantHIVProph{prophNum}MotherHVLHigh', 0)
            self._w(f'InfantHIVProph{prophNum}StopOnPosEID', 0)
            self._w(f'InfantHIVProph{prophNum}AdminProb', *([0.0] * INFANT_PROPH_AGES_NUM))
            self._w(f'InfantHIVProph{prophNum}AdminEIDNegMonths', *([0] * INFANT_PROPH_AGES_NUM))
            self._w(f'InfantHIVProph{prophNum}StartupCost', *([0.0] * INFANT_PROPH_COST_AGES_NUM))
            self._w(f'InfantHIVProph{prophNum}DoseCost', *([0.0] * INFANT_PROPH_COST_AGES_NUM))
            self._w(f'InfantHIVProph{prophNum}EffHorizon', 0)
            self._w(f'InfantHIVProph{prophNum}DecayTime', 0)
            self._w(f'InfantHIVProph{prophNum}ProbSubsequentEff', 0.0)
            # Toxicity: prob, QOLmod, cost, deathRateRatio, duration, deathCost, stopOnTox
            self._w(f'InfantHIVProph{prophNum}MajorTox', 0.0, 1.0, 0.0, 1.0, 0, 0.0, 0)
            self._w(f'InfantHIVProph{prophNum}MinorTox', 0.0, 1.0, 0.0)
            # PP VTHIV multipliers
            self._w(f'InfantHIVProph{prophNum}PPVTHIVThreshold', 0)
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOnARTPre', 'Suppressed', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOnARTPre', 'NotSuppressedLowHVL', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOnARTPre', 'NotSuppressedHighHVL', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOffARTPre', 'EBF', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOffARTPre', 'MBF', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOffARTPre', 'CBF', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOnARTPost', 'Suppressed', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOnARTPost', 'NotSuppressedLowHVL', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOnARTPost', 'NotSuppressedHighHVL', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOffARTPost', 'EBF', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOffARTPost', 'MBF', *([1.0] * PEDS_MATERNAL_STATUS_NUM))
            self._w2(f'InfantHIVProph{prophNum}PPVTHIVMultOffARTPost', 'CBF', *([1.0] * PEDS_MATERNAL_STATUS_NUM))

        # EID HIV Tests (10 tests)
        for testNum in range(EID_NUM_TESTS):
            self._w(f'EIDHIVTest{testNum}CountTowardEIDCosts', 0)
            self._w(f'EIDHIVTest{testNum}ProbOfferedTest', 0.0)
            self._w(f'EIDHIVTest{testNum}ProbAcceptTest', 0.0)
            self._w(f'EIDHIVTest{testNum}TestCost', 0.0)
            self._w(f'EIDHIVTest{testNum}CostResult', 0.0)
            self._w(f'EIDHIVTest{testNum}CostNegResult', 0.0)
            self._w(f'EIDHIVTest{testNum}CostPosResult', 0.0)
            self._w(f'EIDHIVTest{testNum}ResultReturnProbLab', 1.0)
            self._w(f'EIDHIVTest{testNum}ResultReturnProbPatient', 1.0)
            self._w(f'EIDHIVTest{testNum}ResultReturnTime', 0, 0)
            # Sensitivity
            self._w(f'EIDHIVTest{testNum}SensitivityIU', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SensitivityIP', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SensitivityPPBeforeSR', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SensitivityPPAfterSR', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SensitivityPPDuringBF', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SensitivityMultiplierIfMaternalARTPregnancy', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            for prophNum in range(INFANT_HIV_PROPHS_NUM):
                self._w(f'EIDHIVTest{testNum}SensitivityMultiplierInfantHIVProph{prophNum}', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            # Specificity
            self._w(f'EIDHIVTest{testNum}SpecificityHEUBeforeSR', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SpecificityHEUAfterSR', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SpecificityUninfectedMother', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            self._w(f'EIDHIVTest{testNum}SpecificityMotherInfectedBF', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            for prophNum in range(INFANT_HIV_PROPHS_NUM):
                self._w(f'EIDHIVTest{testNum}SpecificityMultiplierInfantHIVProph{prophNum}', *([1.0] * EID_TEST_AGE_CATEGORY_NUM))
            # Confirmatory tests
            self._w(f'EIDHIVTest{testNum}ConfAssay', -1, -1)
            self._w(f'EIDHIVTest{testNum}ConfDelay', 0, 0)
            self._w(f'EIDHIVTest{testNum}ProbLink', 1.0)
            self._w(f'EIDHIVTest{testNum}ProbMaternalStatusBecomeKnownUponResult', 0.0)

    def _gen_adolescent(self):
        """Generate Adolescent section (readAdolescentInputs)."""
        ADOLESCENT_NUM_AGES = 18
        OI_NAMES = [f'OI{i+1}' for i in range(OI_NUM)]

        self._w('EnableAdolescent', 0)
        self._w('TransitionToAdult', 0)
        self._w('AgeTransitionToAdult', 18)
        self._w('AgeTransitionFromPeds', 10)
        self._w('AdolescentAgeBounds', *([0] * (ADOLESCENT_NUM_AGES - 1)))

        # Baseline CD4 decline (by CD4 strata, HVL strata, age categories)
        for cd4 in CD4_STRATA_REV:
            for hvl in HVL_STRATA_REV:
                self._w2(f'BslCD4Decl_Mean_Adolescent_{cd4}', hvl, *([0.0] * ADOLESCENT_NUM_AGES))
            for hvl in HVL_STRATA_REV:
                self._w2(f'BslCD4Decl_StdDev_Adolescent_{cd4}', hvl, *([0.0] * ADOLESCENT_NUM_AGES))

        # OI probabilities (by OI, CD4, history, ART status)
        for oi_name in OI_NAMES:
            for cd4 in CD4_STRATA_REV:
                self._w2(f'Prob_{oi_name}_NoHist_OffART_Adolescent', cd4, *([0.0] * ADOLESCENT_NUM_AGES))
            for cd4 in CD4_STRATA_REV:
                self._w2(f'Prob_{oi_name}_WithHist_OffART_Adolescent', cd4, *([0.0] * ADOLESCENT_NUM_AGES))
        for oi_name in OI_NAMES:
            for cd4 in CD4_STRATA_REV:
                self._w2(f'Prob_{oi_name}_NoHist_OnART_Adolescent', cd4, *([0.0] * ADOLESCENT_NUM_AGES))
            for cd4 in CD4_STRATA_REV:
                self._w2(f'Prob_{oi_name}_WithHist_OnART_Adolescent', cd4, *([0.0] * ADOLESCENT_NUM_AGES))

        # Death rate ratios
        for cd4 in CD4_STRATA_REV:
            self._w2('HIVDthRateRatio_Adolescent', cd4, *([1.0] * ADOLESCENT_NUM_AGES))
        self._w('ARTDthRateRatio_Adolescent', *([1.0] * ADOLESCENT_NUM_AGES))
        for i in range(RISK_FACT_NUM):
            self._w2('GenRiskDthRateRatio_Adolescent', f'Risk{i+1}', *([1.0] * ADOLESCENT_NUM_AGES))
        for cd4 in CD4_STRATA_REV:
            self._w2('AcuteOIDthRateRatio_Adolescent', cd4, *([1.0] * ADOLESCENT_NUM_AGES))
        for cd4 in CD4_STRATA_REV:
            self._w2('AcuteOIDthRateRatioTB_Adolescent', cd4, *([1.0] * ADOLESCENT_NUM_AGES))
        self._w('SevrOI_HistDthRateRatio_Adolescent', *([1.0] * ADOLESCENT_NUM_AGES))
        self._w('SevrOI_HistEffectDuration_Adolescent', 0)
        self._w('TB_OI_HistDthRateRatio_Adolescent', *([1.0] * ADOLESCENT_NUM_AGES))
        self._w('TB_OI_HistEffectDuration_Adolescent', 0)

    def _gen_adolescent_arts(self):
        """Generate AdolescentARTs section (readAdolescentARTInputs)."""
        # Each adolescent ART checks for Id == NOT_APPL (-1) and skips if not specified
        for art_num in range(1, ART_NUM_LINES + 1):
            self._w(f'ART{art_num}IdAYA', -1)  # NOT_APPL = -1


def generate_in_file(params):
    """Generate .in file content from parameters."""
    generator = InputGenerator()
    return generator.generate(params)


def save_in_file(params, filepath):
    """Generate and save .in file."""
    content = generate_in_file(params)
    with open(filepath, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    import sys
    params = {}
    output_path = sys.argv[1] if len(sys.argv) > 1 else 'default.in'
    save_in_file(params, output_path)
    print(f"Generated {output_path}")
