#!/usr/bin/env python3
"""
Script to split the novel "天龙八部" into individual chapter files.
"""

import os
import re

# Get the project root directory (two levels up from script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))

INPUT_FILE = os.path.join(PROJECT_ROOT, "data", "天龙八部 (金庸).txt")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "libs", "chunk", "tian_long_ba_bu")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the input file with BOM handling
with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
    content = f.read()

# Pattern to match chapter titles: 第X章 ...
# Match from beginning of line (or after newline), "第" followed by Chinese numbers and "章"
chapter_pattern = re.compile(r"(^|\n)(第[一二三四五六七八九十百零]+章[^\n]*)(\n|$)")

# Find all chapter positions
chapters = []
for match in chapter_pattern.finditer(content):
    chapters.append({
        'start': match.start(),
        'title_start': match.start() + len(match.group(1)),
        'title': match.group(2),
        'title_end': match.start() + len(match.group(1)) + len(match.group(2)),
        'next_start': match.end()
    })

print(f"Found {len(chapters)} chapters")

# Split the content by chapters
chapter_contents = []
for i, chapter_info in enumerate(chapters):
    if i < len(chapters) - 1:
        # End at the start of next chapter (including the newline after title)
        end = chapters[i + 1]['start']
    else:
        # Last chapter goes to the end of file
        end = len(content)
    
    chapter_title = chapter_info['title']
    chapter_text = content[chapter_info['start']:end]
    chapter_contents.append((chapter_title, chapter_text))

# Write each chapter to a separate file
for i, (title, text) in enumerate(chapter_contents):
    # Clean up the filename - remove invalid characters and extra spaces
    safe_title = re.sub(r'[\\/:*?"<>|\t]+', ' ', title).strip()
    # Remove multiple consecutive spaces
    safe_title = re.sub(r' +', ' ', safe_title)
    filename = f"{i + 1:02d}_{safe_title}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Written: {filename}")

print(f"\nTotal: {len(chapter_contents)} chapter files written to {OUTPUT_DIR}")
