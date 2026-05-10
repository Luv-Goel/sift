# Sift 🔍

<div align="center">

[![PyPI version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://pypi.org/project/sift-dupfinder/)
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-lightgrey.svg)]()
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-blueviolet)]()

**A fast, zero-dependency duplicate file finder.** Scan directories, detect duplicates by content hash, safely deduplicate, and generate beautiful HTML reports.

</div>

---

## ✨ Features

- **Content-based dedup** — Uses SHA-256 hashing to find true duplicates
- **Two-pass scanning** — First groups by size, then hashes only same-sized files (fast!)
- **Safe deduplication** — Dry-run mode to preview before deleting
- **Interactive reports** — Beautiful dark-mode HTML reports with statistics
- **Smart exclusions** — Automatically skips `.git`, `node_modules`, `__pycache__`, binary extensions
- **Pattern filtering** — Exclude files by fnmatch patterns
- **Zero dependencies** — Pure Python 3.8+, no pip requirements

## 📦 Installation

```bash
pip install sift-dupfinder
```

Or install from source:

```bash
git clone https://github.com/Luv-Goel/sift.git
cd sift
pip install -e .
```

## 🚀 Usage

### Scan for duplicates

```bash
# Scan current directory
sift scan

# Scan specific path
sift scan ~/Documents

# Minimum file size filter (skip files under 1KB)
sift scan ~/Downloads --min-size 1024

# Exclude patterns
sift scan ~/Pictures --exclude "*.jpg" --exclude "*thumb*"
```

Output:
```
========================================================
  Duplicate File Scan
========================================================
  Duplicate groups: 12
  Total wasted space: 45,678,912 bytes (43.6 MB)

  [a1b2c3d4e5f6...] 2,048,000 bytes x 3
    Wasted: 4,096,000 bytes
      C:\Users\you\path\to\file-v1.txt
      C:\Users\you\other\copy\file-v1.txt
      C:\Users\you\backup\file-v1.txt
  ...
```

### Generate HTML report

```bash
sift scan ~/Downloads --report duplicates.html
```

Opens a beautiful dark-mode report with summary cards, file listings, and wasted space breakdown.

### Deduplicate files

```bash
# Dry-run (preview what would be deleted)
sift dedupe ~/Downloads --dry-run

# Actually delete duplicates (keeps first occurrence)
sift dedupe ~/Downloads --execute
```

## 📖 CLI Reference

| Command | Description |
|---------|-------------|
| `sift scan [path]` | Scan directory and display duplicate groups |
| `sift scan [path] --report FILE` | Scan and generate HTML report |
| `sift dedupe [path] --dry-run` | Preview deduplication without deleting |
| `sift dedupe [path] --execute` | Deduplicate — keep first, remove rest |
| `sift --version` | Show version information |

### Options

| Option | Applies to | Description |
|--------|-----------|-------------|
| `--min-size BYTES` | scan, dedupe | Minimum file size in bytes (default: 0) |
| `--exclude PATTERN` | scan | Exclude files matching fnmatch pattern (repeatable) |
| `--report FILE` | scan | Generate HTML report at path |
| `--dry-run` | dedupe | Preview deletions without executing |
| `--execute` | dedupe | Actually remove duplicate files |

## 📁 Project Structure

```
sift/
├── sift/
│   ├── __init__.py      # Package info (__version__)
│   ├── cli.py           # CLI argument parsing and orchestration
│   └── core.py          # Scanning, hashing, formatting, HTML report
├── pyproject.toml       # Build configuration
└── README.md
```

## ⚙️ How It Works

1. **First pass**: Walks the directory tree, grouping files by size
2. **Filtering**: Skips common VCS dirs, cache dirs, and binary extensions
3. **Second pass**: SHA-256 hashes only same-sized files (avoids hashing unique files)
4. **Reporting**: Groups duplicates by hash with wasted space calculations

## 🤝 Contributing

Contributions are welcome! This is a learning project — feel free to open issues or PRs for:

- Performance improvements
- Additional hash algorithms (SHA-1, MD5, BLAKE2)
- Parallel scanning support
- GUI frontends

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
