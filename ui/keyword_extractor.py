#!/usr/bin/env python3
"""Extract all keywords from SimContext.cpp and output as JSON."""

import re
import json

def extract_keywords(filepath):
    """Parse SimContext.cpp and extract keywords with context."""

    with open(filepath, 'r') as f:
        content = f.read()

    keywords = []

    # Pattern for readAndSkipPast("keyword", ...)
    p1 = re.compile(r'readAndSkipPast\s*\(\s*"([^"]+)"')
    # Pattern for readAndSkipPast2("kw1", "kw2", ...) or readAndSkipPast2("kw1", VAR, ...)
    p2 = re.compile(r'readAndSkipPast2\s*\(\s*"([^"]+)"\s*,\s*"?([^",\)]+)"?')
    # Pattern for sprintf(buf, "format%d", num) followed by readAndSkipPast
    p_sprintf = re.compile(r'sprintf\s*\(\s*\w+\s*,\s*"([^"]+)"')

    # Track function context
    func_pattern = re.compile(r'void\s+SimContext::(\w+)\s*\(')

    lines = content.split('\n')
    current_func = None

    for i, line in enumerate(lines):
        # Update function context
        m = func_pattern.search(line)
        if m:
            current_func = m.group(1)

        # Check for readAndSkipPast
        m1 = p1.search(line)
        if m1:
            keywords.append({
                'keyword': m1.group(1),
                'func': current_func,
                'line': i + 1,
                'type': 'single'
            })

        # Check for readAndSkipPast2
        m2 = p2.search(line)
        if m2:
            kw2 = m2.group(2).strip()
            # Skip variable references
            if not kw2.startswith(('OI_STRS', 'CD4_STRATA', 'HVL_STRATA',
                                   'RISK_FACT', 'GENDER', 'HIST_OI', 'CHRM_STRS')):
                keywords.append({
                    'keyword': m2.group(1),
                    'keyword2': kw2,
                    'func': current_func,
                    'line': i + 1,
                    'type': 'double'
                })

    return keywords


if __name__ == '__main__':
    keywords = extract_keywords('/workspace/CEPAC/SimContext.cpp')

    # Output as JSON
    with open('/workspace/CEPAC/ui/keywords.json', 'w') as f:
        json.dump(keywords, f, indent=2)

    print(f"Extracted {len(keywords)} keywords to keywords.json")
