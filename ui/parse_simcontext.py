#!/usr/bin/env python3
"""
Parse SimContext.cpp to extract all keywords from readAndSkipPast() calls.
This generates a complete list of keywords in the order they appear.
"""

import re
import sys
from collections import defaultdict

def parse_simcontext(filepath):
    """Parse SimContext.cpp and extract all keywords."""

    with open(filepath, 'r') as f:
        content = f.read()

    # Track which function we're in
    current_function = None
    keywords_by_function = defaultdict(list)
    all_keywords = []

    # Patterns for readAndSkipPast calls
    # readAndSkipPast("keyword", file)
    # readAndSkipPast2("keyword1", "keyword2", file) or readAndSkipPast2("keyword1", VAR, file)
    pattern1 = re.compile(r'readAndSkipPast\s*\(\s*"([^"]+)"')
    pattern2 = re.compile(r'readAndSkipPast2\s*\(\s*"([^"]+)"\s*,\s*"?([^",\)]+)"?')

    # Also capture sprintf + readAndSkipPast patterns
    sprintf_pattern = re.compile(r'sprintf\s*\(\s*\w+\s*,\s*"([^"]+)"')

    # Function definition pattern
    func_pattern = re.compile(r'void\s+SimContext::(\w+)\s*\(')

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Check for function definitions
        func_match = func_pattern.search(line)
        if func_match:
            current_function = func_match.group(1)

        # Check for readAndSkipPast
        match1 = pattern1.search(line)
        if match1:
            keyword = match1.group(1)
            entry = {
                'keyword': keyword,
                'function': current_function,
                'line': i + 1,
                'type': 'single'
            }
            keywords_by_function[current_function].append(entry)
            all_keywords.append(entry)

        # Check for readAndSkipPast2
        match2 = pattern2.search(line)
        if match2:
            keyword1 = match2.group(1)
            keyword2 = match2.group(2)
            entry = {
                'keyword': keyword1,
                'keyword2': keyword2,
                'function': current_function,
                'line': i + 1,
                'type': 'double'
            }
            keywords_by_function[current_function].append(entry)
            all_keywords.append(entry)

    return keywords_by_function, all_keywords


def main():
    if len(sys.argv) < 2:
        filepath = '/workspace/CEPAC/SimContext.cpp'
    else:
        filepath = sys.argv[1]

    keywords_by_function, all_keywords = parse_simcontext(filepath)

    print(f"Total keywords found: {len(all_keywords)}")
    print()

    # Print by function
    for func, keywords in keywords_by_function.items():
        if func:
            print(f"=== {func} ({len(keywords)} keywords) ===")
            for kw in keywords[:10]:  # First 10
                if kw['type'] == 'single':
                    print(f"  {kw['keyword']}")
                else:
                    print(f"  {kw['keyword']} / {kw['keyword2']}")
            if len(keywords) > 10:
                print(f"  ... and {len(keywords) - 10} more")
            print()

    # Generate summary
    print("\n=== Summary by Function ===")
    for func, keywords in keywords_by_function.items():
        if func:
            print(f"{func}: {len(keywords)} keywords")


if __name__ == '__main__':
    main()
