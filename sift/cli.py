"""Sift CLI."""

import argparse
import sys
import os
from . import __version__
from .core import scan_for_duplicates, format_duplicates, generate_report


def main():
    parser = argparse.ArgumentParser(prog="sift", description="Duplicate file finder")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scan", help="Scan for duplicate files")
    p.add_argument("path", nargs="?", default=".", help="Directory to scan")
    p.add_argument("--min-size", type=int, default=0, help="Minimum file size in bytes")
    p.add_argument("--exclude", action="append", default=[], help="Exclude pattern (fnmatch)")
    p.add_argument("--report", metavar="FILE", help="Generate HTML report")

    p = sub.add_parser("dedupe", help="Deduplicate files (keep first, remove rest)")
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--dry-run", action="store_true", help="Show what would be deleted")
    p.add_argument("--execute", action="store_true", help="Actually delete duplicates")
    p.add_argument("--min-size", type=int, default=0)

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"[ERR] Directory not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    if args.command == "scan":
        print(f"  Scanning {args.path} for duplicates...", file=sys.stderr)
        duplicates = scan_for_duplicates(args.path, args.min_size, args.exclude)
        print(format_duplicates(duplicates))
        if args.report:
            path = generate_report(duplicates, args.report)
            print(f"[OK] Report: {path}", file=sys.stderr)

    elif args.command == "dedupe":
        duplicates = scan_for_duplicates(args.path, args.min_size)
        total_freed = 0
        total_removed = 0
        for h, group in sorted(duplicates.items(), key=lambda x: x[1]["wasted_size"], reverse=True):
            files = group["files"]
            keep = files[0]
            for dup in files[1:]:
                total_freed += group["size"]
                total_removed += 1
                if args.execute:
                    try:
                        os.remove(dup)
                        print(f"  Removed: {dup}")
                    except OSError as e:
                        print(f"  [ERR] Could not remove {dup}: {e}", file=sys.stderr)
                else:
                    print(f"  Would remove: {dup}")
        if args.dry_run or not args.execute:
            print(f"\n[Dry Run] Would free {total_freed:,} bytes across {total_removed} files")
        else:
            print(f"\n[OK] Freed {total_freed:,} bytes across {total_removed} files")


if __name__ == "__main__":
    main()
