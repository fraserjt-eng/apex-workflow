#!/usr/bin/env python3
"""
Disproportionality Analysis Script
Calculates risk ratios for equity audits

Usage:
    python disproportionality.py --data file.csv --group column --outcome column

Example:
    python disproportionality.py --data discipline.csv --group race_ethnicity --outcome suspended
"""

import argparse
import pandas as pd
import sys
from typing import Dict

def calculate_risk_ratios(df: pd.DataFrame, group_col: str, outcome_col: str) -> Dict[str, dict]:
    """
    Calculate risk ratios for each group.

    Risk Ratio = (% of group in outcome) / (% of group in population)

    Interpretation:
    - Ratio = 1.0: Proportionate representation
    - Ratio > 1.0: Overrepresentation
    - Ratio < 1.0: Underrepresentation
    """
    results = {}

    total_population = len(df)

    # Handle boolean or numeric outcome column
    if df[outcome_col].dtype == bool:
        total_with_outcome = df[outcome_col].sum()
    else:
        total_with_outcome = len(df[df[outcome_col] == 1])

    for group in df[group_col].unique():
        if pd.isna(group):
            continue

        group_mask = df[group_col] == group
        group_population = group_mask.sum()

        if df[outcome_col].dtype == bool:
            group_with_outcome = df[group_mask & df[outcome_col]].shape[0]
        else:
            group_with_outcome = df[group_mask & (df[outcome_col] == 1)].shape[0]

        # Percentage of group in population
        pop_pct = (group_population / total_population) * 100 if total_population > 0 else 0

        # Percentage of group in outcome
        if total_with_outcome > 0:
            outcome_pct = (group_with_outcome / total_with_outcome) * 100
        else:
            outcome_pct = 0

        # Risk ratio
        if pop_pct > 0:
            risk_ratio = outcome_pct / pop_pct
        else:
            risk_ratio = 0

        # Composition index (alternative measure)
        if group_population > 0:
            group_outcome_rate = (group_with_outcome / group_population) * 100
        else:
            group_outcome_rate = 0

        results[str(group)] = {
            'population_n': int(group_population),
            'population_pct': round(pop_pct, 1),
            'outcome_n': int(group_with_outcome),
            'outcome_pct': round(outcome_pct, 1),
            'outcome_rate': round(group_outcome_rate, 1),
            'risk_ratio': round(risk_ratio, 2)
        }

    return results

def interpret_ratio(ratio: float) -> tuple:
    """Interpret the risk ratio with severity level."""
    if ratio < 0.5:
        return ("Significantly underrepresented", "low")
    elif ratio < 0.8:
        return ("Underrepresented", "low")
    elif ratio <= 1.2:
        return ("Proportionate", "ok")
    elif ratio <= 2.0:
        return ("Overrepresented", "medium")
    elif ratio <= 3.0:
        return ("Significant disproportionality", "high")
    else:
        return ("Severe disproportionality", "critical")

def print_report(results: dict, outcome_name: str):
    """Print formatted disproportionality report."""
    print(f"\n{'='*80}")
    print(f"DISPROPORTIONALITY ANALYSIS REPORT")
    print(f"Outcome: {outcome_name}")
    print(f"{'='*80}\n")

    # Header
    print(f"{'Group':<25} {'Pop %':>8} {'Out %':>8} {'Rate':>8} {'Ratio':>8} {'Assessment':<30}")
    print("-" * 95)

    # Sort by risk ratio (highest first)
    sorted_results = sorted(results.items(), key=lambda x: x[1]['risk_ratio'], reverse=True)

    for group, data in sorted_results:
        interpretation, severity = interpret_ratio(data['risk_ratio'])

        # Severity indicator
        if severity == "critical":
            indicator = "!!!"
        elif severity == "high":
            indicator = "!! "
        elif severity == "medium":
            indicator = "!  "
        else:
            indicator = "   "

        print(f"{group:<25} {data['population_pct']:>7.1f}% {data['outcome_pct']:>7.1f}% "
              f"{data['outcome_rate']:>7.1f}% {data['risk_ratio']:>7.2f}x {indicator}{interpretation:<27}")

    print(f"\n{'='*80}")
    print("INTERPRETATION GUIDE:")
    print("  < 0.5x  = Significantly underrepresented")
    print("  0.5-0.8x = Underrepresented")
    print("  0.8-1.2x = Proportionate (target)")
    print("  1.2-2.0x = Overrepresented (!)")
    print("  2.0-3.0x = Significant disproportionality (!!)")
    print("  > 3.0x  = Severe disproportionality (!!!)")
    print(f"{'='*80}")

    # Highlight concerns
    concerns = [(g, d) for g, d in sorted_results if d['risk_ratio'] > 2.0]
    if concerns:
        print("\nGROUPS REQUIRING IMMEDIATE ATTENTION:")
        for group, data in concerns:
            print(f"  - {group}: {data['risk_ratio']}x overrepresentation "
                  f"({data['outcome_n']} of {data['population_n']} students)")

    print()

def main():
    parser = argparse.ArgumentParser(
        description='Calculate disproportionality ratios for equity analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Discipline analysis:
    python disproportionality.py --data discipline.csv --group race --outcome suspended

  Course access:
    python disproportionality.py --data enrollment.csv --group race --outcome in_ap_course

  With output file:
    python disproportionality.py --data data.csv --group ethnicity --outcome expelled --output results.csv
        """
    )
    parser.add_argument('--data', required=True, help='Path to CSV file')
    parser.add_argument('--group', required=True, help='Column for demographic grouping')
    parser.add_argument('--outcome', required=True, help='Column for outcome (0/1 or boolean)')
    parser.add_argument('--output', help='Output file path for CSV results (optional)')

    args = parser.parse_args()

    # Load data
    try:
        df = pd.read_csv(args.data)
        print(f"\nLoaded {len(df):,} records from {args.data}")
    except FileNotFoundError:
        print(f"Error: File '{args.data}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Validate columns
    if args.group not in df.columns:
        print(f"Error: Column '{args.group}' not found")
        print(f"Available columns: {', '.join(df.columns)}")
        sys.exit(1)

    if args.outcome not in df.columns:
        print(f"Error: Column '{args.outcome}' not found")
        print(f"Available columns: {', '.join(df.columns)}")
        sys.exit(1)

    # Calculate
    results = calculate_risk_ratios(df, args.group, args.outcome)

    # Print report
    print_report(results, args.outcome)

    # Save if output specified
    if args.output:
        results_df = pd.DataFrame(results).T
        results_df.index.name = args.group
        results_df.to_csv(args.output)
        print(f"Results saved to: {args.output}")

if __name__ == "__main__":
    main()
