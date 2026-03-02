from pathlib import Path
from statistics import median
from rich.progress import track

import pymupdf  # PyMuPDF


ORIGINAL_DPI_FALLBACK = 150


def _estimate_page_dpi(page: pymupdf.Page, fallback_dpi: int = ORIGINAL_DPI_FALLBACK) -> int:
    """Estimate page DPI from embedded raster images, or return fallback."""
    image_info = page.get_image_info()
    if not image_info:
        return fallback_dpi

    dpi_values: list[float] = []
    for image in image_info:
        xres = image.get("xres")
        yres = image.get("yres")
        if isinstance(xres, (int, float)) and isinstance(yres, (int, float)) and xres > 0 and yres > 0:
            dpi_values.append((xres + yres) / 2)
            continue

        width_px = image.get("width")
        height_px = image.get("height")
        bbox = image.get("bbox")
        if not (isinstance(width_px, int) and isinstance(height_px, int) and bbox):
            continue

        bbox_width_pt = max(float(bbox[2]) - float(bbox[0]), 1.0)
        bbox_height_pt = max(float(bbox[3]) - float(bbox[1]), 1.0)
        dpi_x = (width_px * 72) / bbox_width_pt
        dpi_y = (height_px * 72) / bbox_height_pt
        dpi_values.append((dpi_x + dpi_y) / 2)

    if not dpi_values:
        return fallback_dpi

    return max(72, min(1200, int(round(median(dpi_values)))))


def create_image_only_pdf(
    input_path: str | Path,
    output_path: str | Path,
    dpi: int | str = 300,
    jpeg_quality: int = 85,
) -> int:
    """Convert a PDF into an image-only PDF and return page count."""
    input_file = Path(input_path)
    output_file = Path(output_path)

    with pymupdf.open(input_file) as doc, pymupdf.open() as new_doc:
        for page_num in track(range(len(doc)), description="Flattening PDF pages..."):
            page = doc.load_page(page_num)

            # 72 DPI is the PDF default; scale to requested output DPI.
            render_dpi = _estimate_page_dpi(page) if dpi == "original" else int(dpi)
            zoom = render_dpi / 72
            matrix = pymupdf.Matrix(zoom, zoom)

            pix = page.get_pixmap(matrix=matrix)
            image_bytes = pix.tobytes("jpeg", jpg_quality=jpeg_quality)

            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(new_page.rect, stream=image_bytes)

        new_doc.save(output_file, garbage=4, deflate=True, clean=True)
        return len(doc)
