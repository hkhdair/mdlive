---
name: mdlive
description: Use when converting, previewing, or generating HTML/PDF from Markdown files. CLI tool for MD→styled HTML, MD→selectable PDF, and live-reload HTTP preview server.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [markdown, html, pdf, preview, conversion, cli]
    related_skills: [powerpoint, ocr-and-documents, ideation]
---

# mdlive — Markdown to HTML/PDF Converter with Live Preview

## Overview

`mdlive` is a Python CLI tool that converts Markdown files to styled HTML or copy-pasteable PDF, with an optional live-reload HTTP server for real-time preview. It uses the `markdown` library (with extensions for tables, fenced code, etc.) and `weasyprint` for professional PDF output with selectable text.

**Repo:** https://github.com/hkhdair/mdlive
**Install:** `pip install git+https://github.com/hkhdair/mdlive.git`

## When to Use

- Converting any `.md` file to a styled HTML document for sharing/embedding
- Generating PDFs from Markdown where text must remain selectable (not image-based)
- Live-previewing Markdown while writing documentation, proposals, or READMEs
- Quick document conversion in automation pipelines

Don't use for:
- Converting to PPTX — use the `powerpoint` skill instead
- Extracting text from scanned PDFs/images — use `ocr-and-documents`

## Quick Command Reference

| Goal | Command |
|---|---|
| HTML to stdout | `mdlive file.md` |
| Save HTML | `mdlive file.md -o output.html` |
| Generate PDF | `mdlive file.md --pdf output.pdf` |
| Live preview (dark) | `mdlive file.md --serve` |
| Live preview (light) | `mdlive file.md --serve --light` |
| Custom port | `mdlive file.md --serve --port 3000` |
| Legacy parser (no deps) | `mdlive file.md --legacy` |

## Features

- **Markdown → HTML**: Full GFM support (tables, fenced code, blockquotes) via `markdown` library
- **Markdown → PDF**: Selectable text, page numbers, professional typography via WeasyPrint
- **Live preview**: HTTP server at `localhost:8080` (default) with auto-reload on file save
- **Dark/light themes**: Default dark mode, `--light` flag for light mode
- **Legacy fallback**: `--legacy` uses pure stdlib parser (no `markdown` dependency needed)

## Dependencies

Required (auto-installed with pip):
- `markdown>=3.4` — proper Markdown parsing with extensions
- `weasyprint>=60.0` — HTML→PDF rendering

System dependencies for WeasyPrint (Ubuntu/Debian):
```bash
sudo apt install libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
```

## Common Pitfalls

1. **WeasyPrint system deps missing**: If PDF generation fails with a library error, install the system packages listed above. pip-installed `weasyprint` needs Cairo/Pango system libs.
2. **Port already in use**: Default port 8080. Use `--port` to change if occupied.
3. **File not found**: Always pass the full or relative path to the `.md` file — `mdlive` doesn't search PATH.
4. **Legacy parser limitations**: The `--legacy` flag uses a basic hand-rolled parser — no table support, no fenced code syntax highlighting. Only use when `markdown` library is unavailable.
5. **Large files**: Very large Markdown files can produce slow PDFs. For big docs, consider splitting or using `--serve` for interactive preview first.

## Verification Checklist

- [ ] `mdlive --help` prints usage
- [ ] `mdlive README.md` outputs HTML to stdout
- [ ] `mdlive README.md -o /tmp/test.html` creates a valid HTML file
- [ ] `mdlive README.md --pdf /tmp/test.pdf` creates a PDF with selectable text
- [ ] `mdlive README.md --serve` starts a server at http://localhost:8080
- [ ] Changing the source file triggers auto-reload in browser
