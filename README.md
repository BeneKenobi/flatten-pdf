# flatten-pdf

`flatten-pdf` converts standard PDFs into image-only PDFs (flattened/rasterized output).

## Features

- Removes selectable text/vector layers by rendering each page to pixels
- Keeps original page dimensions
- Configurable output DPI
- Terminal output powered by `rich`
- CLI powered by `click`

## Requirements

- Python 3.12+
- `uv`

## Setup

```bash
uv sync
```

## Usage

Run as package CLI:

```bash
uv run flatten-pdf INPUT.pdf OUTPUT.pdf --dpi 300
```

JPEG quality defaults to `85` and can be customized:

```bash
uv run flatten-pdf INPUT.pdf OUTPUT.pdf --jpeg-quality 85
uv run flatten-pdf INPUT.pdf OUTPUT.pdf --jpeg-quality 70
```

Keep source-like resolution (estimated from embedded page images):

```bash
uv run flatten-pdf INPUT.pdf OUTPUT.pdf --dpi original
```

If `OUTPUT.pdf` already exists, pass `--overwrite`:

```bash
uv run flatten-pdf INPUT.pdf OUTPUT.pdf --dpi 300 --overwrite
```

Examples:

```bash
uv run flatten-pdf report.pdf report_flattened.pdf
uv run flatten-pdf report.pdf report_flattened.pdf --dpi 200
```

Help:

```bash
uv run flatten-pdf --help
```

## Project structure

```text
src/flatten_pdf/core.py   # PDF flattening logic
src/flatten_pdf/cli.py    # click + rich command line interface
main.py                   # compatibility entrypoint
```
