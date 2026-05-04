#!/usr/bin/env python3
"""
mdlive.py - Markdown to HTML/PDF converter with live preview
Converts markdown files to:
  - Styled HTML (dark/light theme)
  - Editable, copy-paste friendly PDF (selectable text)
  - Live preview via HTTP server with auto-reload

Dependencies: markdown, weasyprint (install: pip install markdown weasyprint)
"""

import argparse
import html
import markdown
import os
import re
import sys
import time
import weasyprint
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


# ─── PDF CSS (print-optimized, copy-paste friendly) ─────────────────────────

PDF_CSS = """
@page {
  size: A4;
  margin: 2.5cm 2cm 2.5cm 2cm;
  @bottom-center {
    content: counter(page);
    font-family: 'DejaVu Sans', sans-serif;
    font-size: 9pt;
    color: #888;
  }
}

body {
  font-family: 'DejaVu Sans', 'Noto Sans', -apple-system, BlinkMacSystemFont,
               'Segoe UI', Roboto, sans-serif;
  font-size: 11pt;
  line-height: 1.65;
  color: #1a1a1a;
  max-width: 100%;
}

h1 {
  font-size: 22pt;
  margin-top: 0;
  margin-bottom: 12pt;
  padding-bottom: 6pt;
  border-bottom: 3px solid #2563eb;
  color: #111;
  page-break-before: always;
}
h1:first-of-type { page-break-before: avoid; }

h2 {
  font-size: 16pt;
  margin-top: 28pt;
  margin-bottom: 10pt;
  padding-bottom: 4pt;
  border-bottom: 1.5px solid #cbd5e1;
  color: #1e293b;
}

h3 {
  font-size: 13pt;
  margin-top: 22pt;
  margin-bottom: 8pt;
  color: #334155;
}

h4, h5, h6 {
  font-size: 11.5pt;
  margin-top: 18pt;
  margin-bottom: 6pt;
  color: #475569;
}

p {
  margin: 8pt 0;
  text-align: justify;
}

a {
  color: #2563eb;
  text-decoration: underline;
}

ul, ol {
  margin: 8pt 0;
  padding-left: 24pt;
}

li {
  margin: 3pt 0;
}

strong {
  color: #111;
}

em {
  color: #334155;
}

blockquote {
  margin: 12pt 0;
  padding: 8pt 16pt;
  border-left: 4px solid #2563eb;
  background: #f1f5f9;
  color: #334155;
  font-style: italic;
}

pre {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 4pt;
  padding: 12pt 14pt;
  margin: 12pt 0;
  overflow-x: auto;
  font-size: 9pt;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
}

code {
  font-family: 'DejaVu Sans Mono', 'Courier New', Consolas, monospace;
  font-size: 9pt;
  background: #f1f5f9;
  padding: 1pt 4pt;
  border-radius: 3pt;
  color: #1e293b;
}

pre code {
  background: none;
  padding: 0;
  border-radius: 0;
  font-size: 9pt;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 12pt 0;
  font-size: 10pt;
}

th, td {
  border: 1px solid #cbd5e1;
  padding: 6pt 10pt;
  text-align: left;
}

th {
  background: #f1f5f9;
  font-weight: 600;
  color: #1e293b;
}

tr:nth-child(even) {
  background: #f8fafc;
}

hr {
  border: none;
  border-top: 1px solid #cbd5e1;
  margin: 20pt 0;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 12pt auto;
}
"""

# ─── HTML theme CSS ─────────────────────────────────────────────────────────

HTML_DARK_CSS = """\
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #1a1a1a;
            color: #e0e0e0;
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            border-bottom: 1px solid #333;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        p { margin: 1em 0; }
        ul, ol { margin: 1em 0; padding-left: 2em; }
        li { margin: 0.5em 0; }
        pre {
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 1em;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1em 0;
        }
        code {
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            background: #333;
            padding: 0.1em 0.3em;
            border-radius: 3px;
        }
        pre code { background: none; padding: 0; }
        a { color: #58a6ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        blockquote {
            border-left: 3px solid #444;
            margin: 1em 0;
            padding: 0.5em 1em;
            color: #999;
        }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #444; padding: 0.5em; text-align: left; }
        th { background: #333; }
"""

HTML_LIGHT_CSS = """\
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #1a1a1a;
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            border-bottom: 1px solid #eee;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        p { margin: 1em 0; }
        ul, ol { margin: 1em 0; padding-left: 2em; }
        li { margin: 0.5em 0; }
        pre {
            background-color: #f6f8fa;
            color: #24292e;
            padding: 1em;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1em 0;
            border: 1px solid #e1e4e8;
        }
        code {
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            background: #f0f0f0;
            padding: 0.1em 0.3em;
            border-radius: 3px;
        }
        pre code { background: none; padding: 0; }
        a { color: #0366d6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        blockquote {
            border-left: 3px solid #ddd;
            margin: 1em 0;
            padding: 0.5em 1em;
            color: #666;
        }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ddd; padding: 0.5em; text-align: left; }
        th { background: #f6f8fa; }
"""


# ─── Markdown → HTML (proper parser) ────────────────────────────────────────

def md_to_html(content, extensions=None):
    """Convert markdown to HTML using the markdown library with extensions.

    Returns clean HTML body content (no <html>/<head>/<body> wrappers).
    """
    if extensions is None:
        extensions = [
            'fenced_code',    # ``` code blocks
            'tables',         # GFM tables
            'toc',            # [TOC] generates table of contents
            'nl2br',          # single newlines → <br>
            'sane_lists',     # better list handling
            'smarty',         # smart quotes, dashes, ellipses
        ]
    return markdown.markdown(content, extensions=extensions)


# ─── HTML wrappers ──────────────────────────────────────────────────────────

def wrap_html(body, title="Markdown Preview", light_theme=False):
    """Wrap HTML body in a full document with theme CSS for live preview."""
    theme_css = HTML_LIGHT_CSS if light_theme else HTML_DARK_CSS
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>{theme_css}
    </style>
</head>
<body>
    {body}
</body>
</html>"""


def wrap_pdf_html(body, title="Document"):
    """Wrap HTML body in a print-optimized document for PDF conversion."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(title)}</title>
    <style>{PDF_CSS}
    </style>
</head>
<body>
    {body}
</body>
</html>"""


# ─── Legacy converter (preserved for --serve basic mode compatibility) ──────

def convert_markdown_to_html(content, light_theme=False):
    """Legacy basic markdown→HTML converter. Kept as fallback.
    Prefer md_to_html() for proper parsing with tables, fenced code, etc.
    """
    html_content = []
    lines = content.split('\n')
    in_code_block = False
    in_list = False

    for line in lines:
        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                html_content.append('<pre><code>')
            else:
                html_content.append('</code></pre>')
            continue

        if in_code_block:
            html_content.append(html.escape(line))
            continue

        if line.startswith('#'):
            level = len(line.split(' ')[0])
            text = line[level:].strip()
            html_content.append(f'<h{level}>{text}</h{level}>')
            continue

        if line.startswith('- '):
            text = line[2:].strip()
            if not in_list:
                html_content.append('<ul>')
                in_list = True
            html_content.append(f'<li>{text}</li>')
            continue
        elif in_list:
            html_content.append('</ul>')
            in_list = False

        if line.strip():
            html_content.append(f'<p>{line}</p>')
        else:
            html_content.append('<br>')

    if in_list:
        html_content.append('</ul>')

    bg_color = "#ffffff" if light_theme else "#1a1a1a"
    text_color = "#000000" if light_theme else "#e0e0e0"
    code_bg = "#f6f8fa" if light_theme else "#2d2d2d"
    code_color = "#24292e" if light_theme else "#f8f8f2"

    html_content_str = '\n'.join(html_content)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Preview</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: {bg_color};
            color: {text_color};
            max-width: 800px;
            margin: 0 auto;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}
        p {{ margin: 1em 0; }}
        ul, ol {{ margin: 1em 0; padding-left: 2em; }}
        li {{ margin: 0.5em 0; }}
        pre {{
            background-color: {code_bg};
            color: {code_color};
            padding: 1em;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1em 0;
        }}
        code {{
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        }}
        a {{ color: #58a6ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    {html_content_str}
</body>
</html>"""


# ─── HTTP Server with live reload ───────────────────────────────────────────

def start_server(port, markdown_file, light_theme=False, use_proper_md=True):
    """Start HTTP server with live reload."""
    class MarkdownHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                current_mtime = os.path.getmtime(markdown_file)
                if current_mtime > getattr(self, 'last_modified', 0):
                    self.last_modified = current_mtime
                    print(f"⟳ File changed at {time.strftime('%H:%M:%S')}")

                try:
                    with open(markdown_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if use_proper_md:
                        body = md_to_html(content)
                        html_content = wrap_html(body,
                            title=os.path.basename(markdown_file),
                            light_theme=light_theme)
                    else:
                        html_content = convert_markdown_to_html(content, light_theme)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_content.encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    error_html = f"<h1>Error</h1><p>{html.escape(str(e))}</p>"
                    self.wfile.write(error_html.encode('utf-8'))
            else:
                super().do_GET()

    MarkdownHandler.markdown_file = markdown_file
    MarkdownHandler.light_theme = light_theme
    MarkdownHandler.use_proper_md = use_proper_md
    MarkdownHandler.last_modified = os.path.getmtime(markdown_file)

    print(f"✓ Server started at http://localhost:{port}")
    print("  Watching for file changes...")
    print("  Press Ctrl+C to stop")
    try:
        HTTPServer(('localhost', port), MarkdownHandler).serve_forever()
    except KeyboardInterrupt:
        print("\n✗ Server stopped")


# ─── PDF conversion ─────────────────────────────────────────────────────────

def md_to_pdf(input_file, output_file):
    """Convert a markdown file to a copy-paste friendly PDF.

    Uses the markdown library for proper MD→HTML parsing (tables, fenced code,
    etc.) and weasyprint for HTML→PDF rendering with selectable text.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert markdown → HTML body
    body = md_to_html(content)

    # Wrap in print-optimized HTML
    html_doc = wrap_pdf_html(body, title=Path(input_file).stem)

    # Render to PDF via weasyprint
    print(f"  Rendering PDF...")
    weasyprint.HTML(string=html_doc).write_pdf(output_file)

    size_kb = os.path.getsize(output_file) / 1024
    print(f"✓ PDF written to {output_file} ({size_kb:.1f} KB)")
    print("  Text is selectable and copy-paste friendly.")


# ─── Main CLI ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown to styled HTML/PDF with live preview",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  mdlive README.md                        # print HTML to stdout
  mdlive README.md -o index.html          # save as HTML
  mdlive README.md --pdf report.pdf       # save as copy-paste friendly PDF
  mdlive README.md --serve --port 3000    # live preview server
  mdlive README.md --serve --light        # light theme server
  mdlive README.md --serve --legacy       # use legacy parser (no deps)
"""
    )
    parser.add_argument('file', help='Markdown file to process')
    parser.add_argument('--output', '-o', metavar='FILE',
                        help='Output HTML file')
    parser.add_argument('--pdf', metavar='FILE',
                        help='Convert to copy-paste friendly PDF (requires weasyprint)')
    parser.add_argument('--serve', '-s', action='store_true',
                        help='Start HTTP server with live reload')
    parser.add_argument('--port', '-p', type=int, default=8080,
                        help='Port for HTTP server (default: 8080)')
    parser.add_argument('--light', action='store_true',
                        help='Use light theme instead of dark (HTML/server only)')
    parser.add_argument('--legacy', action='store_true',
                        help='Use legacy parser (built-in, no markdown library needed)')

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        # ── PDF mode ──
        if args.pdf:
            md_to_pdf(args.file, args.pdf)
            return

        # ── Read file ──
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()

        # ── Convert ──
        if args.legacy:
            html_content = convert_markdown_to_html(content, args.light)
        else:
            body = md_to_html(content)
            html_content = wrap_html(body,
                title=os.path.basename(args.file),
                light_theme=args.light)

        # ── Output ──
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✓ HTML written to {args.output}")
        elif not args.serve:
            print(html_content)

        # ── Serve ──
        if args.serve:
            start_server(args.port, args.file, args.light, use_proper_md=not args.legacy)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
