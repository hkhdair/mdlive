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

## License

MIT — see [LICENSE](LICENSE).
