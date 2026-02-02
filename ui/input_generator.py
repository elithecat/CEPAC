"""
CEPAC Input File Generator

Generates .in files from JSON parameter dictionaries.
The output format matches the keyword-based format expected by SimContext.cpp.
"""

from param_schema import create_default_params, CONSTANTS, CD4_STRATA_STRS, HVL_STRATA_STRS


class InputGenerator:
    """Generator for CEPAC .in input files."""

    def __init__(self):
        self.lines = []

    def generate(self, params):
        """Generate .in file content from parameters dictionary."""
        self.lines = []

        # Generate each section in the order SimContext.cpp reads them
        self._generate_runspecs(params.get('runspecs', {}))
        self._generate_output(params.get('output', {}))
        self._generate_cohort(params.get('cohort', {}))
        self._generate_treatment_part1(params.get('treatment', {}))
        self._generate_arts(params.get('arts', {}))
        self._generate_treatment_part2(params.get('treatment', {}))
        self._generate_prophs(params.get('prophs', {}))
        self._generate_sti(params.get('sti', {}))
        self._generate_ltfu(params.get('ltfu', {}))
        self._generate_heterogeneity(params.get('heterogeneity', {}))
        self._generate_hivtest(params.get('hivtest', {}))
        self._generate_nathist(params.get('nathist', {}))
        self._generate_chrms(params.get('chrms', {}))
        self._generate_qol(params.get('qol', {}))
        self._generate_costs(params.get('costs', {}))
        self._generate_tb(params.get('tb', {}))
        self._generate_peds(params.get('peds', {}))
        self._generate_pedsarts(params.get('pedsarts', {}))
        self._generate_pedscosts(params.get('pedscosts', {}))
        self._generate_eid(params.get('eid', {}))
        self._generate_adolescent(params.get('adolescent', {}))
        self._generate_adolescentarts(params.get('adolescentarts', {}))

        return '\n'.join(self.lines)

    def _w(self, keyword, value):
        """Write a keyword-value line."""
        if isinstance(value, bool):
            self.lines.append(f"{keyword}\t{1 if value else 0}")
        elif isinstance(value, list):
            values = '\t'.join(str(self._format_value(v)) for v in value)
            self.lines.append(f"{keyword}\t{values}")
        else:
            self.lines.append(f"{keyword}\t{self._format_value(value)}")

    def _format_value(self, value):
        """Format a single value for output."""
        if isinstance(value, bool):
            return 1 if value else 0
        elif isinstance(value, float):
            # Format floats with appropriate precision
            if value == int(value):
                return str(int(value))
            return f"{value:.6g}"
        else:
            return str(value)

    def _w_matrix(self, keyword, matrix, row_labels=None):
        """Write a matrix with optional row labels."""
        for i, row in enumerate(matrix):
            if row_labels:
                self._w(f"{keyword}\t{row_labels[i]}", row)
            else:
                self._w(keyword, row)

    def _generate_runspecs(self, p):
        """Generate RunSpecs section."""
        self.lines.append("// RunSpecs Tab")
        self._w("Runset", p.get('runSetName', 'DefaultRunSet'))
        self._w("CohortSize", p.get('numCohorts', 10000))
        self._w("DiscFactor", p.get('discountFactor', 0.03))
        self._w("MaxPatCD4", p.get('maxPatientCD4', 2000.0))

        art_eff = p.get('monthRecordARTEfficacy', [6, 12, 24])
        self._w("MthRecARTEffA", art_eff[0])
        self._w("MthRecARTEffB", art_eff[1])
        self._w("MthRecARTEffC", art_eff[2])

        self._w("RandSeedByTime", p.get('randomSeedByTime', True))
        self._w("UserLocale", p.get('userProgramLocale', 'en_US'))
        self._w("InpVer", p.get('inputVersion', '11.0'))
        self._w("ModelVer", p.get('modelVersion', '11.0'))
        self._w("IncludeTB_AsOI", p.get('OIsIncludeTB', False))
        self._w("OIstrs", p.get('OINames', [f'OI_{i+1}' for i in range(15)]))
        self._w("LongitLogCohort", p.get('longitLoggingLevel', 0))
        self._w("LongitLogFirstOIs", p.get('firstOIsLongitLogging', [0] * 15))
        self._w("LogPriorOIHistProb", p.get('enableOIHistoryLogging', False))
        self._w("LogOIHistwithARTfails", p.get('numARTFailuresForOIHistoryLogging', 0))
        self._w("LogOIHistwithCD4", p.get('CD4BoundsForOIHistoryLogging', [0.0, 2000.0]))
        self._w("LogOIHistwithHVL", p.get('HVLBoundsForOIHistoryLogging', [0, 6]))
        self._w("LogOIHistExcludeOITypes", p.get('OIsToExcludeOIHistoryLogging', [False] * 15))
        self._w("FOB_OIs", p.get('OIsFractionOfBenefit', [1.0] * 15))
        self._w("Severe_OIs", p.get('severeOIs', [False] * 15))
        self._w("CD4Bounds", p.get('CD4StrataUpperBounds', [50.0, 100.0, 200.0, 350.0, 500.0]))
        self._w("EnableMultDiscountOutput", p.get('enableMultipleDiscountRates', False))
        self._w("DiscountRatesCost", p.get('multDiscountRatesCost', [0.0, 0.03, 0.05, 0.07]))
        self._w("DiscountRatesBenefit", p.get('multDiscountRatesBenefit', [0.0, 0.03, 0.05, 0.07]))
        self.lines.append("")

    def _generate_output(self, p):
        """Generate Output section."""
        self.lines.append("// Output Tab")
        self._w("NumPatientsToTrace", p.get('traceNumSelection', 100))
        self._w("EnableSubCohorts", p.get('enableSubCohorts', False))
        self._w("SubCohortValues", p.get('subCohorts', [0] * 25))
        self._w("EnableDetailedCosts", p.get('enableDetailedCostOutputs', False))
        self.lines.append("")

    def _generate_cohort(self, p):
        """Generate Cohort section."""
        self.lines.append("// Cohort Tab")
        self._w("InitCD4", [p.get('initialCD4Mean', 500.0), p.get('initialCD4StdDev', 200.0)])
        self._w("UseSqRtTransform", p.get('enableSquareRootTransform', True))

        # HVL distribution by CD4 stratum
        hvl_dist = p.get('initialHVLDistribution', [[0.0] * 7 for _ in range(6)])
        for j in range(5, -1, -1):
            self.lines.append(f"InitHVL\t{CD4_STRATA_STRS[j]}\t" + '\t'.join(str(v) for v in hvl_dist[j][::-1]))

        self._w("InitAge", [p.get('initialAgeMean', 360.0), p.get('initialAgeStdDev', 120.0)])
        self._w("InitAgeCustomDist", p.get('useCustomAgeDist', False))

        age_strata = p.get('ageStrata', [0.0] * 60)
        self._w("AgeStratMins", age_strata[:30])
        self._w("AgeStratMaxes", age_strata[30:])
        self._w("AgeStratProbs", p.get('ageProbs', [0.0] * 30))

        self._w("InitGender", p.get('maleGenderDistribution', 0.5))
        self._w("ProphNonCompliance", [p.get('OIProphNonComplianceRisk', 0.0),
                                        p.get('OIProphNonComplianceDegree', 0.0)])
        self._w("PatClinicTypes", p.get('clinicVisitTypeDistribution', [0.0, 0.0, 1.0]))
        self._w("PatTreatmentTypes", p.get('therapyImplementationDistribution', [0.0, 0.0, 1.0]))
        self._w("PatCD4ResponeTypeOnART", p.get('CD4ResponseTypeOnARTDistribution', [0.25] * 4))

        # Prior OI history at entry - complex nested structure
        prob_oi_hist = p.get('probOIHistoryAtEntry', [[[0.0] * 15 for _ in range(7)] for _ in range(6)])
        oi_names = p.get('OINames', [f'OI_{i+1}' for i in range(15)])
        for i in range(15):
            self.lines.append(f"PriorOIHistAtEntry\t{oi_names[i]}")
            for k in range(6, -1, -1):
                row = [prob_oi_hist[j][k][i] for j in range(5, -1, -1)]
                self.lines.append(f"\t{HVL_STRATA_STRS[k]}\t" + '\t'.join(str(v) for v in row))

        self._w("ProbRiskFactorPrev", p.get('probRiskFactorPrev', [0.0] * 5))
        self._w("ProbRiskFactorIncid", p.get('probRiskFactorIncid', [0.0] * 5))
        self._w("GenRiskFactorStrs", p.get('riskFactorNames', [f'Risk_{i+1}' for i in range(5)]))

        # Transmission parameters
        self._w("ShowTransmissionOutput", p.get('showTransmissionOutput', False))

        trans_on = p.get('transmRateOnART', [[0.0] * 7 for _ in range(6)])
        for k in range(6, -1, -1):
            row = [trans_on[j][k] for j in range(5, -1, -1)]
            self.lines.append(f"TransmissionRateOnART\t{HVL_STRATA_STRS[k]}\t" + '\t'.join(str(v) for v in row))

        self.lines.append("TransmissionRateOnART\tAcute\t" + '\t'.join(
            str(v) for v in p.get('transmRateOnARTAcute', [0.0] * 6)[::-1]))

        trans_off = p.get('transmRateOffART', [[0.0] * 7 for _ in range(6)])
        for k in range(6, -1, -1):
            row = [trans_off[j][k] for j in range(5, -1, -1)]
            self.lines.append(f"TransmissionRateOffART\t{HVL_STRATA_STRS[k]}\t" + '\t'.join(str(v) for v in row))

        self.lines.append("TransmissionRateOffART\tAcute\t" + '\t'.join(
            str(v) for v in p.get('transmRateOffARTAcute', [0.0] * 6)[::-1]))

        self._w("TransmissionUseHIVTestAcuteDef", p.get('transmUseHIVTestAcuteDefinition', False))
        self._w("TransmissionAcuteDuration", p.get('transmAcuteDuration', 3))
        self._w("IntvlTransmissionRateMultiplier", p.get('transmRateMultInterval', [12, 24]))
        self._w("TransmissionRateMultiplier", p.get('transmRateMult', [1.0, 1.0, 1.0]))

        self._w("UseDynamicTransmission", p.get('useDynamicTransm', False))
        self._w("DynamicTransmissionNumTransmissionsHRG", p.get('dynamicTransmHRGTransmissions', 0.0))
        self._w("DynamicTransmissionPropHRGAttrib", p.get('dynamicTransmPropHRGAttributable', 0.0))
        self._w("DynamicTransmissionNumHIVPosHRG", p.get('dynamicTransmNumHIVPosHRG', 0.0))
        self._w("DynamicTransmissionNumHIVNegHRG", p.get('dynamicTransmNumHIVNegHRG', 0.0))
        self._w("DynamicTransmissionWarmupSize", p.get('dynamicTransmWarmupSize', 0))
        self._w("DynamicTransmissionKeepPrEPAfterWarmup", p.get('keepPrEPAfterWarmup', False))
        self._w("DynamicTransmissionUsePrEPDuringWarmup", p.get('usePrEPDuringWarmup', False))
        self._w("TransmissionUseEndLifeHVLAdjust", p.get('useTransmEndLifeHVLAdjustment', False))
        self._w("TransmissionEndLifeAdjustCD4Threshold", p.get('transmEndLifeHVLAdjustmentCD4Threshold', 0.0))
        self._w("TransmissionEndLifeAdjustARTLineThreshold", p.get('transmEndLifeHVLAdjustmentARTLineThreshold', 0))
        self.lines.append("")

    def _generate_treatment_part1(self, p):
        """Generate Treatment section part 1."""
        self.lines.append("// Treatment Tab - Part 1")
        self._w("IntvlClinicVisit", p.get('clinicVisitInterval', 3))
        self._w("ProbDetOI_Entry", p.get('probDetectOIAtEntry', [0.0] * 15))
        self._w("ProbDetOI_LastVst", p.get('probDetectOISinceLastVisit', [0.0] * 15))
        self._w("ProbSwitchSecProph", p.get('probSwitchSecondaryProph', [0.0] * 15))

        self._w("IntvlCD4Tst_CD4Threshold", p.get('testingIntervalCD4Threshold', 200.0))
        self._w("IntvlCD4Tst_MonthsThreshold", [p.get('testingIntervalARTMonthsThreshold', 6),
                                                 p.get('testingIntervalLastARTMonthsThreshold', 6)])

        cd4_intervals = [
            p.get('CD4TestingIntervalPreARTHighCD4', 6),
            p.get('CD4TestingIntervalPreARTLowCD4', 3),
        ] + p.get('CD4TestingIntervalOnART', [3, 6]) + p.get('CD4TestingIntervalOnLastART', [3, 6]) + [
            p.get('CD4TestingIntervalPostART', 6)
        ]
        self._w("IntvlCD4Tst", cd4_intervals)

        hvl_intervals = [
            p.get('HVLTestingIntervalPreARTHighCD4', 6),
            p.get('HVLTestingIntervalPreARTLowCD4', 3),
        ] + p.get('HVLTestingIntervalOnART', [3, 6]) + p.get('HVLTestingIntervalOnLastART', [3, 6]) + [
            p.get('HVLTestingIntervalPostART', 6)
        ]
        self._w("IntvlHVLTst", hvl_intervals)

        self._w("HVLtestErrProb", [p.get('probHVLTestErrorHigher', 0.0), p.get('probHVLTestErrorLower', 0.0)])
        self._w("CD4testErrSDev", p.get('CD4TestStdDevPercentage', 0.15))
        self._w("CD4testBiasMean", p.get('CD4TestBiasMean', 0.0))
        self._w("CD4testBiasSdev", p.get('CD4TestBiasStdDevPercentage', 0.0))

        self._w("ObsvARTFailTestOnRegClinicVst", p.get('ARTFailureOnlyAtRegularVisit', True))
        self._w("ARTInitHVLTestsWOClinicVst", p.get('numARTInitialHVLTests', 0))
        self._w("ARTInitCD4TestsWOClinicVst", p.get('numARTInitialCD4Tests', 0))
        self._w("OIVstAsNotSchedClinicVst", p.get('emergencyVisitIsNotRegularVisit', False))
        self._w("LagToCD4Test", p.get('CD4TestingLag', 0))
        self._w("LagToHVLTest", p.get('HVLTestingLag', 0))
        self._w("StopCD4MonitoringEnable", p.get('cd4MonitoringStopEnable', False))
        self._w("StopCD4MonitoringThreshold", p.get('cd4MonitoringStopThreshold', 0.0))
        self._w("StopCD4MonitoringMthsPostARTInit", p.get('cd4MonitoringStopMthsPostARTInit', 0))

        # ART start policies
        start_art = p.get('startART', [])
        self.lines.append("ARTstart_CD4\tupp\t" + '\t'.join(
            str(s.get('CD4BoundsOnly', [-1, -1])[1]) for s in start_art[:10]))
        self.lines.append("ARTstart_CD4\tlwr\t" + '\t'.join(
            str(s.get('CD4BoundsOnly', [-1, -1])[0]) for s in start_art[:10]))
        self.lines.append("ARTstart_HVL\tupp\t" + '\t'.join(
            str(s.get('HVLBoundsOnly', [-1, -1])[1]) for s in start_art[:10]))
        self.lines.append("ARTstart_HVL\tlwr\t" + '\t'.join(
            str(s.get('HVLBoundsOnly', [-1, -1])[0]) for s in start_art[:10]))
        self.lines.append("")

    def _generate_treatment_part2(self, p):
        """Generate Treatment section part 2."""
        self.lines.append("// Treatment Tab - Part 2")
        self._w("EnableSTIforART", p.get('enableSTIForART', [False] * 10))
        # Additional treatment parameters would go here
        self.lines.append("")

    def _generate_arts(self, p):
        """Generate ARTs section."""
        self.lines.append("// ARTs Tab")
        art_data = p.get('artData', [])
        for i, art in enumerate(art_data[:10]):
            self.lines.append(f"// ART Line {i + 1}")
            # Simplified - full implementation would include all ART parameters
        self.lines.append("")

    def _generate_prophs(self, p):
        """Generate Prophs section."""
        self.lines.append("// Prophs Tab")
        # Prophylaxis parameters
        self.lines.append("")

    def _generate_sti(self, p):
        """Generate STI section."""
        self.lines.append("// STI Tab")
        # STI parameters
        self.lines.append("")

    def _generate_ltfu(self, p):
        """Generate LTFU section."""
        self.lines.append("// LTFU Tab")
        self._w("UseLTFU", p.get('useLTFU', False))
        self._w("PropRespondLTFUPreART", [p.get('propRespondLTFUPreARTLogitMean', 0.0),
                                           p.get('propRespondLTFUPreARTLogitStdDev', 0.0)])
        self._w("UseInterventionLTFU", p.get('useInterventionLTFU', False))
        self.lines.append("")

    def _generate_heterogeneity(self, p):
        """Generate Heterogeneity section."""
        self.lines.append("// Heterogeneity Tab")
        self._w("PropRespondBaseline", [p.get('propRespondBaselineLogitMean', 0.0),
                                         p.get('propRespondBaselineLogitStdDev', 0.0)])
        self._w("PropRespondAge", p.get('propRespondAge', [0.0] * 7))
        self._w("PropRespondCD4", p.get('propRespondCD4', [0.0] * 6))
        self.lines.append("")

    def _generate_hivtest(self, p):
        """Generate HIVTest section."""
        self.lines.append("// HIVTest Tab")
        self._w("EnableHIVTesting", p.get('enableHIVTesting', False))
        self._w("HIVTestSensitivity", p.get('HIVTestSensitivity', 0.99))
        self._w("HIVTestSpecificity", p.get('HIVTestSpecificity', 0.99))
        self._w("EnablePrEP", p.get('enablePrEP', False))
        self.lines.append("")

    def _generate_nathist(self, p):
        """Generate NatHist section."""
        self.lines.append("// NatHist Tab")
        self._w("HIVDeathRateRatio", p.get('HIVDeathRateRatio', [1.0] * 6))
        self._w("ARTDeathRateRatio", p.get('ARTDeathRateRatio', 1.0))
        self.lines.append("")

    def _generate_chrms(self, p):
        """Generate CHRMs section."""
        self.lines.append("// CHRMs Tab")
        self._w("ShowCHRMsOutput", p.get('showCHRMsOutput', False))
        self._w("EnableOrphans", p.get('enableOrphans', False))
        self.lines.append("")

    def _generate_qol(self, p):
        """Generate QOL section."""
        self.lines.append("// QOL Tab")
        self._w("QOLCalculationType", p.get('QOLCalculationType', 0))
        self.lines.append("")

    def _generate_costs(self, p):
        """Generate Costs section."""
        self.lines.append("// Costs Tab")
        self._w("CostAgeBounds", p.get('costAgeBounds', [18, 25, 35, 45, 55, 65]))
        self.lines.append("")

    def _generate_tb(self, p):
        """Generate TB section."""
        self.lines.append("// TB Tab")
        self._w("EnableTB", p.get('enableTB', False))
        self.lines.append("")

    def _generate_peds(self, p):
        """Generate Peds section."""
        self.lines.append("// Peds Tab")
        self._w("EnablePediatrics", p.get('enablePediatrics', False))
        self.lines.append("")

    def _generate_pedsarts(self, p):
        """Generate PedsARTs section."""
        self.lines.append("// PedsARTs Tab")
        self.lines.append("")

    def _generate_pedscosts(self, p):
        """Generate PedsCosts section."""
        self.lines.append("// PedsCosts Tab")
        self.lines.append("")

    def _generate_eid(self, p):
        """Generate EID section."""
        self.lines.append("// EID Tab")
        self._w("EnableEID", p.get('enableEID', False))
        self.lines.append("")

    def _generate_adolescent(self, p):
        """Generate Adolescent section."""
        self.lines.append("// Adolescent Tab")
        self._w("EnableAdolescent", p.get('enableAdolescent', False))
        self.lines.append("")

    def _generate_adolescentarts(self, p):
        """Generate AdolescentARTs section."""
        self.lines.append("// AdolescentARTs Tab")
        self.lines.append("")


def generate_in_file(params):
    """Convenience function to generate .in file content."""
    generator = InputGenerator()
    return generator.generate(params)


def save_in_file(params, filepath):
    """Generate and save .in file."""
    content = generate_in_file(params)
    with open(filepath, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    import sys
    from param_schema import create_default_params

    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = 'default.in'

    params = create_default_params()
    save_in_file(params, output_path)
    print(f"Generated {output_path}")
