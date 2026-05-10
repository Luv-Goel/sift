# Sift ðŸ”

<div align="center">

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-lightgrey)]()
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-blueviolet)]()

**A fast, zero-dependency duplicate file finder â€” scan, hash, deduplicate, and generate beautiful HTML reports.**

</div>

---

## Features

- **Content-based dedup** â€” SHA-256 hashing to find true duplicates, not just same-named files
- **Two-pass scanning** â€” Groups by file size first, then hashes only same-sized candidates (fast!)
- **Safe deduplication** â€” Dry-run mode previews what would be deleted before you commit
- **Dark-mode HTML reports** â€” Beautiful interactive reports with wasted space breakdowns
- **Smart exclusions** â€” Skips `.git`, `node_modules`, `__pycache__`, binary extensions automatically
- **Pattern filtering** â€” Exclude files with fnmatch patterns
- **Zero external dependencies** â€” Pure Python 3.8+, stdlib only

## Quick Start

```bash
pip install sift-dupfinder

# Scan current directory
sift scan

# Generate HTML report
sift scan ~/Downloads --report duplicates.html

# Preview what would be deleted
sift dedupe ~/Downloads --dry-run

# Actually remove duplicates
sift dedupe ~/Downloads --execute
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `sift scan [path]` | Scan directory for duplicate files |
| `sift scan --report FILE` | Scan and generate analysis report |
| `sift dedupe --dry-run` | Preview deduplication changes |
| `sift dedupe --execute` | Remove duplicate files (keeps first) |

### Options

| Flag | Description |
|------|-------------|
| `--min-size BYTES` | Minimum file size to consider (default: 0) |
| `--exclude PATTERN` | Exclude files matching pattern (repeatable) |
| `--report FILE` | Output HTML report path |

## How It Works

1. **First pass** â€” Walks the directory tree, groups files by size
2. **Filter** â€” Skips VCS dirs, caches, and binary extensions
3. **Second pass** â€” SHA-256 hashes only same-sized files (skips unique files)
4. **Report** â€” Groups duplicates by hash with wasted space calculations

## Project Structure

```
sift/
â”œâ”€â”€ sift/
â”‚   â”œâ”€â”€ __init__.py    # Package info
â”‚   â”œâ”€â”€ cli.py         # Argument parsing + orchestration
â”‚   â””â”€â”€ core.py        # Scanning, hashing, report generation
â”œâ”€â”€ pyproject.toml
â””â”€â”€ README.md
```

## License

MIT â€” see [LICENSE](LICENSE).
