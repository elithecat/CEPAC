#!/usr/bin/env python3
"""
CEPAC Automated Code Review Script

This script performs chunk-by-chunk code review of CEPAC source files using
the Claude API. It generates a structured review report.

Usage:
    python code_review.py [--output report.md]

Requirements:
    - anthropic Python package
    - ANTHROPIC_API_KEY environment variable
"""

import os
import sys
import json
import glob
import argparse
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)


# Configuration
CHUNK_SIZE = 300  # Lines per chunk
MODEL = "claude-sonnet-4-20250514"
CEPAC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_source_files():
    """Get all C++ source files."""
    cpp_files = glob.glob(os.path.join(CEPAC_DIR, "*.cpp"))
    h_files = glob.glob(os.path.join(CEPAC_DIR, "*.h"))
    return sorted(cpp_files + h_files)


def chunk_file(filepath, chunk_size=CHUNK_SIZE):
    """Split a file into chunks of approximately chunk_size lines."""
    with open(filepath, 'r') as f:
        lines = f.readlines()

    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = {
            'start_line': i + 1,
            'end_line': min(i + chunk_size, len(lines)),
            'content': ''.join(lines[i:i + chunk_size])
        }
        chunks.append(chunk)

    return chunks


def review_chunk(client, filepath, chunk, review_type):
    """Review a single code chunk."""
    filename = os.path.basename(filepath)

    if review_type == 'code':
        prompt = f"""Review this C++ code chunk from {filename} (lines {chunk['start_line']}-{chunk['end_line']}) for:
1. Potential bugs and logic errors
2. Memory management issues (leaks, dangling pointers, null pointers)
3. Error handling gaps
4. Code quality issues
5. Performance concerns

Be specific and cite line numbers. Focus on actual issues, not style preferences.

Code:
```cpp
{chunk['content']}
```

Respond in JSON format:
{{
    "issues": [
        {{"severity": "high|medium|low", "line": N, "description": "...", "suggestion": "..."}}
    ],
    "summary": "Brief summary"
}}"""

    else:  # epi review
        prompt = f"""Review this C++ code chunk from {filename} (lines {chunk['start_line']}-{chunk['end_line']}) for epidemiological/modeling concerns:
1. Biological plausibility of disease progression logic
2. Mathematical correctness of probability calculations
3. Rate-to-probability conversions
4. Parameter bounds and validation
5. Model state transitions

This is an HIV/AIDS microsimulation model (CEPAC). Focus on epidemiological accuracy.

Code:
```cpp
{chunk['content']}
```

Respond in JSON format:
{{
    "concerns": [
        {{"category": "biological|mathematical|implementation", "line": N, "description": "...", "recommendation": "..."}}
    ],
    "summary": "Brief summary"
}}"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        text = response.content[0].text
        # Try to find JSON in the response
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        return {"error": "No valid JSON in response"}

    except Exception as e:
        return {"error": str(e)}


def review_file(client, filepath, review_type='code'):
    """Review an entire file."""
    print(f"  Reviewing {os.path.basename(filepath)}...")

    chunks = chunk_file(filepath)
    results = {
        'filename': os.path.basename(filepath),
        'filepath': filepath,
        'total_lines': sum(c['end_line'] - c['start_line'] + 1 for c in chunks),
        'chunks': []
    }

    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i+1}/{len(chunks)} (lines {chunk['start_line']}-{chunk['end_line']})")
        review = review_chunk(client, filepath, chunk, review_type)
        results['chunks'].append({
            'start_line': chunk['start_line'],
            'end_line': chunk['end_line'],
            'review': review
        })

    return results


def aggregate_results(code_results, epi_results):
    """Aggregate results into categorized findings."""
    findings = {
        'critical': [],
        'medium': [],
        'low': [],
        'epi_concerns': [],
        'by_file': {}
    }

    for result in code_results:
        filename = result['filename']
        findings['by_file'][filename] = {'code': [], 'epi': []}

        for chunk in result['chunks']:
            review = chunk.get('review', {})
            if 'error' in review:
                continue

            for issue in review.get('issues', []):
                severity = issue.get('severity', 'low')
                issue['file'] = filename
                issue['chunk_lines'] = f"{chunk['start_line']}-{chunk['end_line']}"

                if severity == 'high':
                    findings['critical'].append(issue)
                elif severity == 'medium':
                    findings['medium'].append(issue)
                else:
                    findings['low'].append(issue)

                findings['by_file'][filename]['code'].append(issue)

    for result in epi_results:
        filename = result['filename']
        if filename not in findings['by_file']:
            findings['by_file'][filename] = {'code': [], 'epi': []}

        for chunk in result['chunks']:
            review = chunk.get('review', {})
            if 'error' in review:
                continue

            for concern in review.get('concerns', []):
                concern['file'] = filename
                concern['chunk_lines'] = f"{chunk['start_line']}-{chunk['end_line']}"
                findings['epi_concerns'].append(concern)
                findings['by_file'][filename]['epi'].append(concern)

    return findings


def generate_report(findings, output_path):
    """Generate markdown report."""
    report = []
    report.append("# CEPAC Code Review Report")
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Executive Summary
    report.append("## Executive Summary\n")
    report.append(f"- **Critical Issues**: {len(findings['critical'])}")
    report.append(f"- **Medium Issues**: {len(findings['medium'])}")
    report.append(f"- **Minor Issues**: {len(findings['low'])}")
    report.append(f"- **Epidemiological Concerns**: {len(findings['epi_concerns'])}")
    report.append(f"- **Files Reviewed**: {len(findings['by_file'])}\n")

    # Critical Issues
    if findings['critical']:
        report.append("## Critical Issues\n")
        for issue in findings['critical']:
            report.append(f"### {issue['file']}:{issue.get('line', '?')}")
            report.append(f"**Description**: {issue.get('description', 'N/A')}")
            report.append(f"**Suggestion**: {issue.get('suggestion', 'N/A')}\n")

    # Medium Issues
    if findings['medium']:
        report.append("## Medium Issues\n")
        for issue in findings['medium']:
            report.append(f"- **{issue['file']}:{issue.get('line', '?')}**: {issue.get('description', 'N/A')}")

    # Epidemiological Concerns
    if findings['epi_concerns']:
        report.append("\n## Epidemiological Concerns\n")
        for concern in findings['epi_concerns']:
            report.append(f"### {concern['file']}:{concern.get('line', '?')}")
            report.append(f"**Category**: {concern.get('category', 'N/A')}")
            report.append(f"**Description**: {concern.get('description', 'N/A')}")
            report.append(f"**Recommendation**: {concern.get('recommendation', 'N/A')}\n")

    # File-by-file summary
    report.append("## File-by-File Summary\n")
    for filename, file_findings in sorted(findings['by_file'].items()):
        code_count = len(file_findings['code'])
        epi_count = len(file_findings['epi'])
        if code_count > 0 or epi_count > 0:
            report.append(f"### {filename}")
            report.append(f"- Code issues: {code_count}")
            report.append(f"- Epi concerns: {epi_count}\n")

    # Write report
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))

    print(f"\nReport written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='CEPAC Automated Code Review')
    parser.add_argument('--output', '-o', default='docs/code_review_report.md',
                        help='Output report path')
    parser.add_argument('--skip-epi', action='store_true',
                        help='Skip epidemiological review')
    parser.add_argument('--files', nargs='+', help='Specific files to review')
    args = parser.parse_args()

    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Get files to review
    if args.files:
        source_files = [os.path.join(CEPAC_DIR, f) for f in args.files]
    else:
        source_files = get_source_files()

    print(f"Found {len(source_files)} source files to review")

    # Code review
    print("\n=== Code Quality Review ===")
    code_results = []
    for filepath in source_files:
        result = review_file(client, filepath, 'code')
        code_results.append(result)

    # Epidemiological review
    epi_results = []
    if not args.skip_epi:
        print("\n=== Epidemiological Review ===")
        # Focus on key epi-related files
        epi_files = [f for f in source_files if any(x in f for x in [
            'Updater', 'SimContext', 'Patient', 'Mortality', 'CD4', 'HVL', 'TB', 'OI'
        ])]
        for filepath in epi_files:
            result = review_file(client, filepath, 'epi')
            epi_results.append(result)

    # Aggregate and report
    print("\n=== Generating Report ===")
    findings = aggregate_results(code_results, epi_results)

    output_path = os.path.join(CEPAC_DIR, args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generate_report(findings, output_path)

    # Also save raw results as JSON
    json_path = output_path.replace('.md', '.json')
    with open(json_path, 'w') as f:
        json.dump({
            'code_results': code_results,
            'epi_results': epi_results,
            'findings': findings
        }, f, indent=2)
    print(f"Raw results saved to: {json_path}")


if __name__ == '__main__':
    main()
