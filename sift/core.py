"""Sift — Duplicate file finder core."""

import os
import hashlib
import json
from typing import List, Dict, Optional
from collections import defaultdict


SKIP_DIRS = {".git", ".svn", "__pycache__", "node_modules", ".venv", ".eggs", "dist", "build"}
SKIP_EXTS = {".pyc", ".o", ".so", ".dll", ".dylib", ".exe"}


def hash_file(path: str, algo: str = "sha256") -> str:
    """Quick hash a file."""
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def get_size(path: str) -> int:
    return os.path.getsize(path)


def scan_for_duplicates(root: str, min_size: int = 0, exclude_patterns: List[str] = None) -> Dict[str, List[Dict]]:
    """Scan directory for duplicate files by content hash."""
    exclude = exclude_patterns or []

    def is_excluded(name):
        for pat in exclude:
            import fnmatch
            if fnmatch.fnmatch(name, pat):
                return True
        return False

    # First pass: group by size
    by_size = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if is_excluded(fn):
                continue
            path = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext in SKIP_EXTS:
                continue
            try:
                size = get_size(path)
                if size >= min_size:
                    by_size[size].append(path)
            except OSError:
                pass

    # Second pass: hash files with same size
    by_hash = defaultdict(list)
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        for path in paths:
            try:
                file_hash = hash_file(path)
                by_hash[file_hash].append({
                    "path": path,
                    "size": size,
                })
            except OSError:
                pass

    # Group duplicates
    duplicates = {}
    for file_hash, files in by_hash.items():
        if len(files) >= 2:
            duplicates[file_hash] = {
                "hash": file_hash,
                "size": files[0]["size"],
                "total_size": files[0]["size"] * len(files),
                "wasted_size": files[0]["size"] * (len(files) - 1),
                "files": [f["path"] for f in files],
                "count": len(files),
            }

    return duplicates


def format_duplicates(duplicates: Dict, max_groups: int = 50) -> str:
    """Format duplicate groups as text."""
    if not duplicates:
        return "  [OK] No duplicates found."

    sorted_groups = sorted(duplicates.values(),
                            key=lambda g: g["wasted_size"], reverse=True)
    total_wasted = sum(g["wasted_size"] for g in sorted_groups)

    lines = ["=" * 56, "  Duplicate File Scan", "=" * 56]
    lines.append(f"  Duplicate groups: {len(sorted_groups)}")
    lines.append(f"  Total wasted space: {total_wasted:,} bytes ({total_wasted/1024/1024:.1f} MB)")
    lines.append("")

    for group in sorted_groups[:max_groups]:
        lines.append(f"  [{group['hash'][:12]}...] {group['size']:,} bytes x {group['count']}")
        lines.append(f"    Wasted: {group['wasted_size']:,} bytes")
        for path in group['files']:
            lines.append(f"      {path}")
        lines.append("")

    if len(sorted_groups) > max_groups:
        lines.append(f"  ... and {len(sorted_groups) - max_groups} more groups")

    return "\n".join(lines)


def generate_report(duplicates: Dict, output_path: str) -> str:
    """Generate HTML report."""
    sorted_groups = sorted(duplicates.values(),
                            key=lambda g: g["wasted_size"], reverse=True)
    total_wasted = sum(g["wasted_size"] for g in sorted_groups)
    total_groups = len(sorted_groups)
    total_dupe_files = sum(g["count"] - 1 for g in sorted_groups)

    rows = ""
    for g in sorted_groups[:100]:
        rows += f"<tr><td><code>{g['hash'][:12]}...</code></td><td>{g['count']}</td><td>{g['size']:,}</td><td>{g['wasted_size']:,}</td><td style='font-size:0.8rem'>"
        for path in g['files'][:5]:
            rows += f"{path}<br>"
        if len(g['files']) > 5:
            rows += f"... +{len(g['files'])-5} more"
        rows += "</td></tr>\n"

    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Sift Report</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f172a;color:#e2e8f0;padding:2rem}}
h1{{font-size:2rem}}
.meta{{color:#94a3b8;margin:0.5rem 0 1.5rem}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem}}
.stat{{background:#1e293b;padding:1rem;border-radius:0.75rem}}
.stat-value{{font-size:1.5rem;font-weight:700}}
.stat-label{{font-size:0.8rem;color:#94a3b8}}
.card{{background:#1e293b;border-radius:0.75rem}}
.card-body{{padding:1rem}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;padding:0.5rem;background:#1e293b;border-bottom:2px solid #334155;font-size:0.8rem}}
td{{padding:0.5rem;border-bottom:1px solid #334155;font-size:0.85rem}}
code{{color:#f87171}}
</style></head><body>
<h1>Duplicate File Report</h1>
<p class="meta">Generated by Sift</p>
<div class="grid">
<div class="stat"><div class="stat-value">{total_groups}</div><div class="stat-label">Duplicate Groups</div></div>
<div class="stat"><div class="stat-value">{total_dupe_files}</div><div class="stat-label">Duplicate Files</div></div>
<div class="stat"><div class="stat-value">{total_wasted/1024/1024:.1f} MB</div><div class="stat-label">Wasted Space</div></div>
</div>
<div class="card"><div class="card-body">
<table><thead><tr><th>Hash</th><th>Copies</th><th>Size</th><th>Wasted</th><th>Locations</th></tr></thead><tbody>{rows}</tbody></table>
</div></div>
<p style="margin-top:2rem;color:#64748b;font-size:0.8rem;">Sift — Duplicate File Finder</p>
</body></html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path
