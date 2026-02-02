"""
CEPAC Input File Parser

Parses .in files into JSON format compatible with the UI.
The .in format is keyword-based text where keywords mark the start of data sections.
"""

import re
import copy
from param_schema import create_default_params, CONSTANTS, KEYWORD_MAP


class InputParser:
    """Parser for CEPAC .in input files."""

    def __init__(self):
        self.params = None
        self.tokens = []
        self.pos = 0

    def parse_file(self, filepath):
        """Parse a .in file and return parameter dictionary."""
        with open(filepath, 'r') as f:
            content = f.read()
        return self.parse_content(content)

    def parse_content(self, content):
        """Parse .in file content string and return parameter dictionary."""
        # Start with defaults
        self.params = create_default_params()

        # Tokenize the content
        self.tokens = self._tokenize(content)
        self.pos = 0

        # Parse by finding keywords and reading their associated values
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            if self._is_keyword(token):
                self._parse_keyword_section(token)
            else:
                self.pos += 1

        return self.params

    def _tokenize(self, content):
        """Split content into tokens (whitespace-separated, handling strings)."""
        # Remove comments (lines starting with # or //)
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove // comments
            if '//' in line:
                line = line[:line.index('//')]
            # Remove # comments (but not inside strings)
            if '#' in line and not ('"' in line or "'" in line):
                line = line[:line.index('#')]
            cleaned_lines.append(line)

        content = '\n'.join(cleaned_lines)

        # Split on whitespace
        tokens = content.split()
        return tokens

    def _is_keyword(self, token):
        """Check if token is a known keyword."""
        # Known keywords from SimContext.cpp readAndSkipPast calls
        keywords = set(KEYWORD_MAP.keys())

        # Also check for composite keywords like "ARTstart_CD4"
        for kw in list(keywords):
            if token.startswith(kw.split('_')[0]):
                return True

        return token in keywords

    def _parse_keyword_section(self, keyword):
        """Parse a section starting with a keyword."""
        self.pos += 1  # Move past keyword

        # Map keyword to parameter path
        if keyword in KEYWORD_MAP:
            tab, path = KEYWORD_MAP[keyword]
            self._read_value_for_path(tab, path)
        else:
            # Handle special/complex keywords
            self._handle_special_keyword(keyword)

    def _read_value_for_path(self, tab, path):
        """Read value(s) and store in the appropriate parameter path."""
        if tab not in self.params:
            return

        # Simple path (no array notation)
        if '[' not in path:
            param = self.params[tab].get(path)
            if param is None:
                return

            if isinstance(param, bool):
                self.params[tab][path] = self._read_bool()
            elif isinstance(param, int):
                self.params[tab][path] = self._read_int()
            elif isinstance(param, float):
                self.params[tab][path] = self._read_float()
            elif isinstance(param, str):
                self.params[tab][path] = self._read_string()
            elif isinstance(param, list):
                self._read_list_into(self.params[tab], path)

    def _read_list_into(self, parent, key):
        """Read values into a list parameter."""
        lst = parent.get(key)
        if lst is None or not isinstance(lst, list):
            return

        n = len(lst)
        for i in range(n):
            if self.pos >= len(self.tokens):
                break

            if isinstance(lst[i], bool):
                lst[i] = self._read_bool()
            elif isinstance(lst[i], int):
                lst[i] = self._read_int()
            elif isinstance(lst[i], float):
                lst[i] = self._read_float()
            elif isinstance(lst[i], str):
                lst[i] = self._read_string()
            elif isinstance(lst[i], list):
                # Nested list - read recursively
                self._read_nested_list(lst[i])

    def _read_nested_list(self, lst):
        """Read values into a nested list."""
        for i in range(len(lst)):
            if self.pos >= len(self.tokens):
                break

            if isinstance(lst[i], bool):
                lst[i] = self._read_bool()
            elif isinstance(lst[i], int):
                lst[i] = self._read_int()
            elif isinstance(lst[i], float):
                lst[i] = self._read_float()
            elif isinstance(lst[i], str):
                lst[i] = self._read_string()
            elif isinstance(lst[i], list):
                self._read_nested_list(lst[i])

    def _read_bool(self):
        """Read a boolean value."""
        if self.pos >= len(self.tokens):
            return False
        token = self.tokens[self.pos]
        self.pos += 1

        # Handle various boolean representations
        if token.lower() in ('true', '1', 'yes', 'y'):
            return True
        elif token.lower() in ('false', '0', 'no', 'n'):
            return False
        else:
            try:
                return int(token) != 0
            except ValueError:
                return False

    def _read_int(self):
        """Read an integer value."""
        if self.pos >= len(self.tokens):
            return 0
        token = self.tokens[self.pos]
        self.pos += 1

        try:
            return int(token)
        except ValueError:
            try:
                return int(float(token))
            except ValueError:
                return 0

    def _read_float(self):
        """Read a float value."""
        if self.pos >= len(self.tokens):
            return 0.0
        token = self.tokens[self.pos]
        self.pos += 1

        try:
            return float(token)
        except ValueError:
            return 0.0

    def _read_string(self):
        """Read a string value."""
        if self.pos >= len(self.tokens):
            return ''
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _handle_special_keyword(self, keyword):
        """Handle complex keywords that need special parsing."""
        # Skip unknown keywords - just move past them
        # In a complete implementation, we'd handle all the special cases
        # like "ARTstart_CD4 upp", "InitHVL CD4vhi", etc.
        pass

    def skip_past(self, keyword):
        """Skip tokens until finding the specified keyword."""
        while self.pos < len(self.tokens):
            if self.tokens[self.pos] == keyword:
                self.pos += 1
                return True
            self.pos += 1
        return False


def parse_in_file(filepath):
    """Convenience function to parse a .in file."""
    parser = InputParser()
    return parser.parse_file(filepath)


def parse_in_content(content):
    """Convenience function to parse .in content string."""
    parser = InputParser()
    return parser.parse_content(content)


if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) > 1:
        params = parse_in_file(sys.argv[1])
        print(json.dumps(params, indent=2))
    else:
        print("Usage: python input_parser.py <input.in>")
