import os
import re
import glob
from datetime import datetime, date, timedelta

# --------------------------------------------------#
# DEFAULT CONFIG
# --------------------------------------------------#

PATTERN_CONFIG = {
    "reference_pattern": r'(\d{8}|\d{2}-[A-Za-z]+-\d{4}|\d{2}-\d{2}-\d{4}|\d{4}-\d{2}-\d{2})',
    "candidate_pattern": r'(\d{8}|\d{2}-[A-Za-z]+-\d{4}|\d{2}-\d{2}-\d{4}|\d{4}-\d{2}-\d{2})'
}

DEFAULT_DATE_FORMAT = "%d%m%Y"

# --------------------------------------------------#
# DATE PARSER (AUTO)
# --------------------------------------------------#

def parse_date_auto(date_str: str) -> date:
    formats = [
        "%d%m%Y",
        "%Y%m%d",
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d/%m/%Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")

# --------------------------------------------------#
# FILE LOADER (recursive / non-recursive)
# --------------------------------------------------#

def _get_files(folder, recursive=False):
    if recursive:
        return glob.glob(os.path.join(folder, "**", "*"), recursive=True)
    return glob.glob(os.path.join(folder, "*"))

# --------------------------------------------------#
# REFERENCE DATE EXTRACTION
# --------------------------------------------------#

def extract_max_reference_date(
    reference_folder,
    reference_pattern=None,
    reference_recursive=False
):
    pattern = re.compile(reference_pattern or PATTERN_CONFIG["reference_pattern"])
    dates = []

    for file_path in _get_files(reference_folder, reference_recursive):
        fname = os.path.basename(file_path)

        match = pattern.search(fname)
        if match:
            try:
                dates.append(parse_date_auto(match.group(1)))
            except ValueError:
                continue

    if not dates:
        raise ValueError("No valid reference files found.")

    return max(dates)

# --------------------------------------------------#
# CANDIDATE FILTER
# --------------------------------------------------#

def filter_candidate_files(
    candidate_folder,
    start_date,
    end_date,
    candidate_pattern=None,
    candidate_recursive=False
):
    pattern = re.compile(candidate_pattern or PATTERN_CONFIG["candidate_pattern"])
    filtered_files = []

    for file_path in _get_files(candidate_folder, candidate_recursive):
        fname = os.path.basename(file_path)

        match = pattern.search(fname)
        if not match:
            continue

        try:
            file_date = parse_date_auto(match.group(1))
        except ValueError:
            continue

        if start_date <= file_date <= end_date:
            filtered_files.append(file_path)

    return filtered_files

# --------------------------------------------------#
# MAIN ENGINE
# --------------------------------------------------#

def get_filtered_files(
    reference_folder,
    candidate_folder,
    reference_pattern=None,
    candidate_pattern=None,
    reference_recursive=False,
    candidate_recursive=False
):
    """
    Get filtered files based on reference max date + 1 to yesterday.

    Args:
        reference_folder (str):
            ⚠ REQUIRED. Folder containing reference files used to extract max processed date.

        candidate_folder (str):
            ⚠ REQUIRED. Folder containing candidate files to be filtered.

        reference_pattern (str, optional):
            ✔ OPTIONAL. Regex pattern to extract date from reference files.
            If None, default pattern is used.

        candidate_pattern (str, optional):
            ✔ OPTIONAL. Regex pattern to extract date from candidate files.
            If None, default pattern is used.

        reference_recursive (bool, optional):
            ✔ OPTIONAL. If True, searches reference folder recursively (includes subfolders).
            Default is False.

        candidate_recursive (bool, optional):
            ✔ OPTIONAL. If True, searches candidate folder recursively (includes subfolders).
            Default is False.

    Returns:
        list:
            Filtered file paths within valid date range.
    
    📌 Example:
    
        filtered_files = get_filtered_files(
            reference_folder="D:/TXN/Pure_TNL",
            candidate_folder="D:/LTE/KPIs",
            reference_pattern=r'\\d+_TNL_EX_Outage_.*?(\\d{8}|\\d{2}-[A-Za-z]+-\\d{4}|\\d{2}-\\d{2}-\\d{4}|\\d{4}-\\d{2}-\\d{2}).*',
            candidate_pattern=r'LTE_Cell_Hourly_.*_(\\d{8}|\\d{2}-[A-Za-z]+-\\d{4}|\\d{2}-\\d{2}-\\d{4}|\\d{4}-\\d{2}-\\d{2}).*',
            reference_recursive=False,
            candidate_recursive=False
        )

        print(filtered_files)
    
    """
    max_date = extract_max_reference_date(
        reference_folder,
        reference_pattern,
        reference_recursive
    )

    yesterday = date.today() - timedelta(days=1)

    if max_date >= yesterday:
        return []

    start_date = max_date + timedelta(days=1)

    return filter_candidate_files(
        candidate_folder,
        start_date,
        yesterday,
        candidate_pattern,
        candidate_recursive
    )
