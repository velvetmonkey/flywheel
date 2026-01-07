"""
OKR Scoring Algorithm Tests (v1.8.0)

Tests for the okr-review-agent's scoring algorithm that calculates progress
on key results using a 0-1.0 scale.

Formula: score = (current - baseline) / (target - baseline)
Clamped to [0.0, 1.0]

Test cases:
1. Fully achieved (current = target) → 1.0
2. Half achieved (current = midpoint) → 0.5
3. Exceeded (current > target) → 1.0 (capped)
4. Zero progress (current = baseline) → 0.0
5. Regression (current < baseline) → 0.0 (floored)
"""

import pytest


def calculate_okr_score(baseline: float, target: float, current: float) -> float:
    """
    Calculate OKR key result score on 0-1.0 scale.

    Args:
        baseline: Starting point value
        target: Goal value
        current: Current achieved value

    Returns:
        Score from 0.0 to 1.0

    Formula:
        score = (current - baseline) / (target - baseline)

    Edge cases:
        - If current >= target: return 1.0 (fully achieved)
        - If current <= baseline: return 0.0 (no progress)
        - If baseline == target: return 1.0 if current >= target else 0.0
    """
    # Avoid division by zero
    if target == baseline:
        return 1.0 if current >= target else 0.0

    # Calculate raw score
    raw_score = (current - baseline) / (target - baseline)

    # Clamp to [0.0, 1.0]
    return max(0.0, min(1.0, raw_score))


class TestOKRScoringAlgorithm:
    """Test OKR scoring calculation formula."""

    def test_fully_achieved(self):
        """Current equals target → score = 1.0"""
        baseline = 100
        target = 200
        current = 200

        score = calculate_okr_score(baseline, target, current)

        assert score == 1.0, "Reaching target should score 1.0"

    def test_half_achieved(self):
        """Current at midpoint → score = 0.5"""
        baseline = 100
        target = 200
        current = 150  # Midpoint between 100 and 200

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.5, "Midpoint progress should score 0.5"

    def test_exceeded_target(self):
        """Current exceeds target → score = 1.0 (capped)"""
        baseline = 100
        target = 200
        current = 250  # 50 above target

        score = calculate_okr_score(baseline, target, current)

        assert score == 1.0, "Exceeding target should be capped at 1.0"

    def test_zero_progress(self):
        """Current equals baseline → score = 0.0"""
        baseline = 100
        target = 200
        current = 100  # No progress from baseline

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.0, "No progress should score 0.0"

    def test_regression_below_baseline(self):
        """Current below baseline → score = 0.0 (floored)"""
        baseline = 100
        target = 200
        current = 50  # Regressed 50 below baseline

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.0, "Regression should be floored at 0.0"


class TestOKRScoringEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_same_baseline_and_target(self):
        """Baseline equals target → binary scoring"""
        baseline = 100
        target = 100
        current = 100

        score = calculate_okr_score(baseline, target, current)

        assert score == 1.0, "When baseline=target and current=target, score 1.0"

    def test_same_baseline_target_below(self):
        """Baseline equals target, current below → score 0.0"""
        baseline = 100
        target = 100
        current = 50

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.0, "When baseline=target and current<target, score 0.0"

    def test_negative_values(self):
        """Handle negative baseline/target/current"""
        baseline = -50
        target = 50
        current = 0  # Midpoint

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.5, "Should handle negative values correctly"

    def test_decreasing_goal(self):
        """Target < baseline (e.g., reduce costs)"""
        baseline = 1000  # Start at $1000/month
        target = 500    # Goal: reduce to $500/month
        current = 750   # Currently at $750/month

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.5, "Decreasing goals should calculate correctly"

    def test_decimal_precision(self):
        """Score should maintain decimal precision"""
        baseline = 0
        target = 3
        current = 1

        score = calculate_okr_score(baseline, target, current)

        assert abs(score - 0.333333) < 0.01, "Should preserve decimal precision"


class TestOKRScoringRealWorld:
    """Test with real-world OKR scenarios."""

    def test_revenue_growth_okr(self):
        """Real example: Grow MRR from $10K to $25K"""
        baseline = 10000   # Current MRR
        target = 25000     # Goal MRR
        current = 18000    # Achieved MRR

        score = calculate_okr_score(baseline, target, current)

        # (18000 - 10000) / (25000 - 10000) = 8000 / 15000 = 0.533
        assert abs(score - 0.533) < 0.01, "Revenue growth should calculate correctly"

    def test_customer_acquisition_okr(self):
        """Real example: Acquire 100 new customers (from 0)"""
        baseline = 0
        target = 100
        current = 75

        score = calculate_okr_score(baseline, target, current)

        assert score == 0.75, "Customer acquisition should score 0.75"

    def test_bug_reduction_okr(self):
        """Real example: Reduce bugs from 50 to 10"""
        baseline = 50
        target = 10
        current = 30  # Reduced to 30 bugs

        score = calculate_okr_score(baseline, target, current)

        # (30 - 50) / (10 - 50) = -20 / -40 = 0.5
        assert score == 0.5, "Bug reduction should score 0.5"

    def test_nps_improvement_okr(self):
        """Real example: Improve NPS from 30 to 60"""
        baseline = 30
        target = 60
        current = 50

        score = calculate_okr_score(baseline, target, current)

        # (50 - 30) / (60 - 30) = 20 / 30 = 0.666
        assert abs(score - 0.666) < 0.01, "NPS improvement should score 0.666"


class TestOKRMultipleKeyResults:
    """Test scoring multiple key results and averaging."""

    def test_average_okr_score(self):
        """Average score across 3 key results"""
        key_results = [
            {"baseline": 0, "target": 100, "current": 100},  # 1.0
            {"baseline": 0, "target": 50, "current": 25},    # 0.5
            {"baseline": 0, "target": 200, "current": 100},  # 0.5
        ]

        scores = [
            calculate_okr_score(kr["baseline"], kr["target"], kr["current"])
            for kr in key_results
        ]

        average_score = sum(scores) / len(scores)

        assert average_score == 0.666666666, "Average should be 0.67 (rounded)"

    def test_weighted_okr_score(self):
        """Weighted average where KRs have different importance"""
        key_results = [
            {"baseline": 0, "target": 100, "current": 50, "weight": 0.5},   # 0.5 * 0.5 = 0.25
            {"baseline": 0, "target": 50, "current": 50, "weight": 0.3},    # 1.0 * 0.3 = 0.30
            {"baseline": 0, "target": 200, "current": 100, "weight": 0.2},  # 0.5 * 0.2 = 0.10
        ]

        weighted_score = sum(
            calculate_okr_score(kr["baseline"], kr["target"], kr["current"]) * kr["weight"]
            for kr in key_results
        )

        assert weighted_score == 0.65, "Weighted average should be 0.65"


class TestOKRConfidenceAdjustment:
    """Test confidence-adjusted scoring (optional extension)."""

    def test_high_confidence_score(self):
        """High confidence in data → use raw score"""
        baseline = 0
        target = 100
        current = 75
        confidence = 1.0  # 100% confident

        raw_score = calculate_okr_score(baseline, target, current)
        adjusted_score = raw_score * confidence

        assert adjusted_score == 0.75

    def test_low_confidence_score(self):
        """Low confidence in data → discount score"""
        baseline = 0
        target = 100
        current = 75
        confidence = 0.6  # Only 60% confident

        raw_score = calculate_okr_score(baseline, target, current)
        adjusted_score = raw_score * confidence

        assert adjusted_score == 0.45, "Low confidence should discount score"
