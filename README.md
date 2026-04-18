# File Filter Utils

A Python utility for filtering files based on dates extracted from filenames.

## Features
- Auto-detect multiple date formats
- Extract max reference date
- Filter candidate files between date ranges
- Supports recursive and non-recursive search

## Installation

```bash
pip install git+https://github.com/your-username/file-filter-utils.git

# Usage
from file_filter import get_filtered_files

filtered_files = get_filtered_files(
    reference_folder="D:/TXN/Pure_TNL",
    candidate_folder="D:/LTE/KPIs"
)

print(filtered_files)
