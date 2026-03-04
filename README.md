# flatten-pdf

Convert PDFs into image-only (rasterized) PDFs.

Features
- Renders each page to an image and produces an output PDF with the same page dimensions
- Configurable DPI (`72–1200` or `original`) and JPEG quality
- Simple CLI with clear error handling

Requirements
- Python 3.12+

Usage

Run the console command (the repo includes a `flatten-pdf` script):

```bash
uv run flatten-pdf INPUT.pdf OUTPUT.pdf [--dpi 300] [--jpeg-quality 85] [--overwrite]
```

Examples

```bash
uv run flatten-pdf report.pdf report_flattened.pdf
uv run flatten-pdf report.pdf report_flattened.pdf --dpi 200 --overwrite
```

Help

```bash
uv run flatten-pdf --help
```
