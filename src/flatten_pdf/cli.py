from pathlib import Path

import click
from rich.console import Console

from .core import create_image_only_pdf

console = Console()


class DpiParamType(click.ParamType):
    name = "dpi"

    def convert(self, value: object, param: click.Parameter | None, ctx: click.Context | None) -> int | str:
        if isinstance(value, int):
            if 72 <= value <= 1200:
                return value
            self.fail("DPI must be between 72 and 1200.", param, ctx)

        normalized = str(value).strip().lower()
        if normalized == "original":
            return "original"

        try:
            parsed = int(normalized)
        except ValueError:
            self.fail("DPI must be an integer (72-1200) or 'original'.", param, ctx)

        if not (72 <= parsed <= 1200):
            self.fail("DPI must be between 72 and 1200.", param, ctx)

        return parsed


DPI_TYPE = DpiParamType()


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("input_file", type=click.Path(path_type=Path, exists=True, dir_okay=False))
@click.argument("output_file", type=click.Path(path_type=Path, dir_okay=False))
@click.option("--dpi", type=DPI_TYPE, default="original", show_default=True)
@click.option("--jpeg-quality", type=click.IntRange(1, 100), default=85, show_default=True)
@click.option("--overwrite/--no-overwrite", default=False, show_default=True)
def main(input_file: Path, output_file: Path, dpi: int | str, jpeg_quality: int, overwrite: bool) -> None:
    """Flatten INPUT_FILE into an image-only PDF and write to OUTPUT_FILE."""

    if input_file.resolve() == output_file.resolve():
        console.print("[bold red]Error:[/bold red] Input and output paths must be different.")
        raise click.Abort()

    if output_file.exists() and not overwrite:
        console.print(
            "[bold red]Error:[/bold red] Output file already exists. "
            "Use [bold]--overwrite[/bold] to replace it."
        )
        raise click.Abort()

    if output_file.exists() and overwrite:
        output_file.unlink()

    try:
        pages = create_image_only_pdf(input_file, output_file, dpi=dpi, jpeg_quality=jpeg_quality)
    except Exception as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise click.Abort() from exc

    console.print(f"[bold green]Done.[/bold green] Converted {pages} page(s) to [italic]{output_file}[/italic].")


if __name__ == "__main__":
    main()
