from pathlib import Path
from subprocess import CalledProcessError, run

from loguru import logger
from typer import Typer, echo

BASE_DIR = Path(__file__).parent

main = Typer()


def _export(
    *,
    notebook_path: Path,
    output_dir: Path,
) -> bool:
    output_path = output_dir / notebook_path.with_suffix(".html").name

    args = [
        "uv",
        "run",
        "marimo",
        "export",
        "html-wasm",
        str(notebook_path),
        "-o",
        str(output_path),
        "--mode",
        "run",
        "--no-show-code",
        # "--include-cloudflare",
    ]

    try:
        run(
            args,
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except CalledProcessError as e:
        logger.error(f"Error exporting {notebook_path}:")
        logger.error(e.stderr)
        return False
    except Exception as e:
        logger.error(f"Unexpected error {notebook_path}:")
        logger.error(e)
        return True


@main.command()
def build_wasm_html(
    notebook_dir: Path = BASE_DIR / "notebooks",
    output_dir: Path = BASE_DIR / "_site",
) -> None:
    errors = [
        not _export(
            notebook_path=notebook_fn,
            output_dir=output_dir,
        )
        for notebook_fn in notebook_dir.glob("*.py")
    ]

    n_errors = sum(errors)
    n_total = len(errors)
    frac_errors = n_errors / n_total

    if n_errors != 0:
        echo(
            f"The export failed for {n_errors} / {n_total} ({frac_errors:.1%}) notebooks. Increase the log level for more details."
        )
        exit(1)

    echo("Export succeeded without any errors.")


if __name__ == "__main__":
    main()
