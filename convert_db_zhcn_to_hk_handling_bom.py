#!/usr/bin/env python3
"""
Batch-convert all *_zh-CN.json files under a given directory to Hong Kong Traditional Chinese in-place.
Handles files with UTF-8 BOM correctly.
Usage:
  python convert_db_zhcn_to_hk.py --db-dir ./assets/databases --pattern '*_zh-CN.json' [--debug]
"""
import argparse
import glob
import json
import logging
from pathlib import Path

from opencc import OpenCC


def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='[%(levelname)s] %(message)s')


def convert_value(value, cc: OpenCC):
    """
    Recursively convert string values in JSON data structures.
    """
    if isinstance(value, str):
        return cc.convert(value)
    elif isinstance(value, list):
        return [convert_value(v, cc) for v in value]
    elif isinstance(value, dict):
        return {k: convert_value(v, cc) for k, v in value.items()}
    else:
        return value


def process_file(path: Path, cc: OpenCC):
    logging.info(f"Processing file: {path}")
    try:
        # Read using utf-8-sig to strip BOM if present
        text = path.read_text(encoding='utf-8-sig')
        data = json.loads(text)
    except Exception as e:
        logging.error(f"Failed to parse JSON in {path}: {e}")
        return

    converted = convert_value(data, cc)
    # Write back in place without BOM
    path.write_text(json.dumps(converted, ensure_ascii=False, indent=2), encoding='utf-8')
    logging.info(f"Saved converted file: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--db-dir', '-d', default='./assets/databases',
        help='Directory containing the JSON files'
    )
    parser.add_argument(
        '--pattern', '-p', default='*_zh-CN.json',
        help='Glob pattern for JSON files'
    )
    parser.add_argument(
        '--debug', action='store_true', help='Enable debug logging'
    )
    args = parser.parse_args()

    setup_logging(args.debug)
    cc = OpenCC('s2hk')  # Simplified Chinese → Hong Kong Traditional

    db_path = Path(args.db_dir)
    if not db_path.is_dir():
        logging.error(f"Directory not found: {db_path}")
        return

    files = glob.glob(str(db_path / args.pattern))
    if not files:
        logging.warning(f"No files matched pattern: {args.pattern}")
        return

    for f in files:
        process_file(Path(f), cc)


if __name__ == '__main__':
    main()
