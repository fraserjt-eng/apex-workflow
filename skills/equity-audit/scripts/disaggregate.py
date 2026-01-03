#!/usr/bin/env python3
"""
Data Disaggregation Script
Breaks down aggregate data by demographic categories with intersectional analysis

Usage:
    python disaggregate.py --data file.csv --by "race,gender,sped,ell"
    python disaggregate.py --data file.csv --by "race,gender" --metric gpa --intersect

Example:
    python disaggregate.py --data students.csv --by "race_ethnicity,gender,sped_status" --metric math_score
"""

import argparse
import pandas as pd
import sys
from itertools import combinations

def disaggregate_single(df: pd.DataFrame, by_col: str, metric_col: str = None) -> pd.DataFrame:
    """Disaggregate by a single column."""
    if metric_col and metric_col in df.columns:
        result = df.groupby(by_col).agg({
            metric_col: ['count', 'mean', 'std', 'min', 'max']
        }).round(2)
        result.columns = ['Count', 'Mean', 'Std Dev', 'Min', 'Max']
    else:
        result = df.groupby(by_col).size().reset_index(name='Count')
        result['Percent'] = (result['Count'] / result['Count'].sum() * 100).round(1)
        result = result.set_index(by_col)

    return result

def disaggregate_intersectional(df: pd.DataFrame, cols: list, metric_col: str = None) -> pd.DataFrame:
    """Disaggregate by intersection of multiple columns."""
    if metric_col and metric_col in df.columns:
        result = df.groupby(cols).agg({
            metric_col: ['count', 'mean', 'std']
        }).round(2)
        result.columns = ['Count', 'Mean', 'Std Dev']
    else:
        result = df.groupby(cols).size().reset_index(name='Count')
        result['Percent'] = (result['Count'] / result['Count'].sum() * 100).round(1)

    return result

def print_single_disaggregation(df: pd.DataFrame, col: str, result: pd.DataFrame, metric: str = None):
    """Print single-variable disaggregation."""
    print(f"\n{'='*60}")
    print(f"DISAGGREGATION BY: {col.upper()}")
    print(f"{'='*60}")

    total = result['Count'].sum() if 'Count' in result.columns else len(df)
    print(f"Total Records: {total:,}\n")

    if metric:
        print(f"Metric: {metric}\n")
        print(result.to_string())
    else:
        for idx, row in result.iterrows():
            pct = row.get('Percent', row['Count']/total*100)
            bar = '#' * int(pct / 2)
            print(f"  {idx:<30} {row['Count']:>6,} ({pct:>5.1f}%) {bar}")

    print()

def print_intersectional(result: pd.DataFrame, cols: list, metric: str = None):
    """Print intersectional analysis."""
    print(f"\n{'='*60}")
    print(f"INTERSECTIONAL ANALYSIS: {' x '.join([c.upper() for c in cols])}")
    print(f"{'='*60}\n")

    if metric:
        print(f"Metric: {metric}\n")

    print(result.to_string())
    print()

def identify_gaps(df: pd.DataFrame, by_col: str, metric_col: str) -> list:
    """Identify significant gaps in outcomes."""
    if metric_col not in df.columns:
        return []

    grouped = df.groupby(by_col)[metric_col].mean()
    overall_mean = df[metric_col].mean()
    overall_std = df[metric_col].std()

    gaps = []
    for group, mean in grouped.items():
        diff = mean - overall_mean
        if overall_std > 0:
            effect_size = diff / overall_std
            if abs(effect_size) > 0.5:  # Medium effect size threshold
                gaps.append({
                    'group': group,
                    'mean': round(mean, 2),
                    'overall_mean': round(overall_mean, 2),
                    'difference': round(diff, 2),
                    'effect_size': round(effect_size, 2),
                    'direction': 'above' if diff > 0 else 'below'
                })

    return sorted(gaps, key=lambda x: abs(x['effect_size']), reverse=True)

def main():
    parser = argparse.ArgumentParser(
        description='Disaggregate data by demographic categories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic disaggregation:
    python disaggregate.py --data students.csv --by "race,gender"

  With outcome metric:
    python disaggregate.py --data students.csv --by "race,gender,sped" --metric test_score

  Intersectional analysis:
    python disaggregate.py --data students.csv --by "race,gender" --metric gpa --intersect

  Full analysis with output:
    python disaggregate.py --data students.csv --by "race,gender,ell,sped" --metric math_score --intersect --output results.csv
        """
    )
    parser.add_argument('--data', required=True, help='Path to CSV file')
    parser.add_argument('--by', required=True, help='Comma-separated columns to disaggregate by')
    parser.add_argument('--metric', help='Metric column to analyze (optional)')
    parser.add_argument('--intersect', action='store_true', help='Include intersectional analysis')
    parser.add_argument('--gaps', action='store_true', help='Identify significant outcome gaps')
    parser.add_argument('--output', help='Output file path (optional)')

    args = parser.parse_args()

    # Load data
    try:
        df = pd.read_csv(args.data)
        print(f"\n{'#'*60}")
        print(f"# DATA DISAGGREGATION REPORT")
        print(f"# Source: {args.data}")
        print(f"# Records: {len(df):,}")
        print(f"{'#'*60}")
    except FileNotFoundError:
        print(f"Error: File '{args.data}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Parse columns
    by_cols = [col.strip() for col in args.by.split(',')]

    # Validate columns
    missing = [col for col in by_cols if col not in df.columns]
    if missing:
        print(f"Error: Columns not found: {', '.join(missing)}")
        print(f"Available columns: {', '.join(df.columns)}")
        sys.exit(1)

    if args.metric and args.metric not in df.columns:
        print(f"Warning: Metric column '{args.metric}' not found, proceeding without metric")
        args.metric = None

    # Single-variable disaggregation
    all_results = {}
    for col in by_cols:
        result = disaggregate_single(df, col, args.metric)
        all_results[col] = result
        print_single_disaggregation(df, col, result, args.metric)

        # Gap analysis
        if args.gaps and args.metric:
            gaps = identify_gaps(df, col, args.metric)
            if gaps:
                print(f"  SIGNIFICANT GAPS DETECTED:")
                for gap in gaps:
                    direction = "+" if gap['direction'] == 'above' else ""
                    print(f"    - {gap['group']}: {gap['mean']} ({direction}{gap['difference']}, "
                          f"effect size: {gap['effect_size']})")
                print()

    # Intersectional analysis
    if args.intersect and len(by_cols) >= 2:
        for r in range(2, min(len(by_cols) + 1, 4)):  # Limit to 3-way intersections
            for cols in combinations(by_cols, r):
                result = disaggregate_intersectional(df, list(cols), args.metric)
                print_intersectional(result, list(cols), args.metric)

    # Summary
    print(f"\n{'='*60}")
    print("EQUITY ANALYSIS NOTES:")
    print("="*60)
    print("- Compare outcome rates across groups, not just raw counts")
    print("- Consider systemic factors when interpreting gaps")
    print("- Use intersectional analysis to reveal hidden disparities")
    print("- Pair quantitative data with qualitative (street data)")
    print("="*60 + "\n")

    # Save if output specified
    if args.output:
        with pd.ExcelWriter(args.output) if args.output.endswith('.xlsx') else open(args.output, 'w') as f:
            for col, result in all_results.items():
                if args.output.endswith('.xlsx'):
                    result.to_excel(f, sheet_name=col[:31])
                else:
                    f.write(f"\n=== {col} ===\n")
                    f.write(result.to_csv())
        print(f"Results saved to: {args.output}")

if __name__ == "__main__":
    main()
