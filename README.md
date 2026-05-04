# mdlive

**Markdown to HTML/PDF converter with live preview — a zero-hassle CLI tool.**

[![PyPI](https://img.shields.io/badge/pip%20install-mdlive-blue)](https://github.com/hkhdair/mdlive)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

## Features

- **Markdown → styled HTML** — dark or light theme, responsive layout
- **Markdown → selectable PDF** — copy-paste friendly, professional formatting (tables, code blocks, page numbers)
- **Live preview server** — auto-reloads on save, just edit and watch
- **Zero config** — sensible defaults, works out of the box

## Quick Start

```bash
pip install git+https://github.com/hkhdair/mdlive.git
```

```bash
# Print styled HTML to stdout
mdlive README.md

# Save as HTML file
mdlive README.md -o index.html

# Convert to PDF (selectable text, professional styling)
mdlive README.md --pdf report.pdf

# Start live preview server (auto-reload on save)
mdlive README.md --serve

# Light theme
mdlive README.md --serve --light

# Custom port
mdlive README.md --serve --port 3000
```

## Requirements

- Python 3.8+
- `pip install markdown weasyprint` (auto-installed with `pip install`)

> **Debian/Ubuntu users:** If you get `externally-managed-environment`, use:
> ```bash
> pip install --break-system-packages git+https://github.com/hkhdair/mdlive.git
> ```
> Or use `pipx`:
> ```bash
> pipx install git+https://github.com/hkhdair/mdlive.git
> ```

## Hermes Agent Skill

This repo includes a `SKILL.md` — a reusable skill for [Hermes Agent](https://hermes-agent.nousresearch.com/docs) that teaches it how to use `mdlive` automatically.

### What it does

When the skill is installed, Hermes will automatically use `mdlive` whenever you ask it to:

- Convert Markdown to HTML or PDF
- Start a live preview of a Markdown file
- Generate styled documents from Markdown

No need to remember command flags — just say *"convert this to a PDF"* and Hermes handles it.

### How to install

```bash
# Copy the skill into Hermes' skills directory
mkdir -p ~/.hermes/skills/productivity/mdlive
cp SKILL.md ~/.hermes/skills/productivity/mdlive/
```

Or clone the whole repo and symlink:

```bash
git clone https://github.com/hkhdair/mdlive.git
ln -s "$(pwd)/mdlive/SKILL.md" ~/.hermes/skills/productivity/mdlive/SKILL.md
```

### When it triggers

Hermes auto-loads the skill when your request involves any of these:

| You say... | Hermes does... |
|---|---|
| *"Convert this to HTML"* | `mdlive file.md -o file.html` |
| *"Make a PDF from this README"* | `mdlive README.md --pdf output.pdf` |
| *"Start a live preview"* | `mdlive file.md --serve` |
| *"I want light theme"* | Adds `--light` flag |
| *"Use port 3000"* | Adds `--port 3000` |

The skill also knows about pitfalls (missing WeasyPrint system deps, port conflicts) and will fix them proactively rather than failing silently.

## License

MIT — see [LICENSE](LICENSE).
