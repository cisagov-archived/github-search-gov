#!/usr/bin/env python3 -u
"""Analyze code at URLs to determine reference types."""


# Standard Python Libraries
import re
import sys

# Third-Party Libraries
import requests


def classify_usage(line):
    """
    Classify how tj-actions/changed-files is used in a line.

    Look for a pattern like:
      uses: tj-actions/changed-files[@<version>]
    and return the classification:
      - "unpinned" if no version is provided.
      - "pinned by sha" if version is a 40-character hexadecimal string.
      - "pinned by tag" otherwise.
    """
    # Regex explanation:
    #   - Look for "uses:" followed by optional whitespace,
    #   - then the literal "tj-actions/changed-files"
    #   - then optionally an "@" and one or more non-whitespace characters.
    m = re.search(r"uses:\s*tj-actions/changed-files(?:@([^\s]+))?", line)
    if m:
        version = m.group(1)
        if not version:
            return "unpinned"
        # Check if version looks like a SHA (40 hex characters)
        if len(version) == 40 and all(c in "0123456789abcdefABCDEF" for c in version):
            return "pinned by sha"
        else:
            return "pinned by tag"
    return None


def process_url(url):
    """
    Process a GitHub URL.

    Convert a GitHub blob URL to raw, fetch file content, and print lines
    that reference tj-actions/changed-files with a classification.
    """
    raw_url = url.replace("/blob/", "/raw/")
    try:
        resp = requests.get(raw_url, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {raw_url}: {e}")
        return

    lines = resp.text.splitlines()
    found = False
    for i, line in enumerate(lines, start=1):
        classification = classify_usage(line)
        if classification:
            found = True
            print(f"Line {i}: {line.strip()} ({classification})")
    if not found:
        print("No usage of tj-actions/changed-files found.")


def main():
    """Process URLs from a file."""
    if len(sys.argv) != 2:
        print("Usage: analyse-urls.py urls.txt")
        sys.exit(1)

    urls_file = sys.argv[1]
    try:
        with open(urls_file) as f:
            urls = f.readlines()
    except Exception as e:
        print(f"Error reading file {urls_file}: {e}")
        sys.exit(1)

    print(f"# Processing {len(urls)} lines from {urls_file}")
    for line in urls:
        line = line.strip()
        # Skip empty lines or comments
        if not line or line.startswith("#"):
            continue
        print(f"\nProcessing URL: {line}")
        process_url(line)
        print("-" * 40)


if __name__ == "__main__":
    main()
