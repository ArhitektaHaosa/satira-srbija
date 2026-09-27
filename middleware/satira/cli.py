from __future__ import annotations

import json

import typer

from satira.pipeline import run, setup_logging

cli = typer.Typer(add_completion=False, no_args_is_help=True)


@cli.command()
def draft(idea: str, push: bool = typer.Option(True, help="Create a WordPress draft")) -> None:
    setup_logging()
    result = run(idea, push=push)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
    raise typer.Exit(0 if result.get("ok") else 1)


@cli.command()
def validate_only(path: str) -> None:
    from pathlib import Path

    from satira.validator import validate_article

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_article(payload)
    typer.echo(json.dumps({"errors": errors}, ensure_ascii=False, indent=2))
    raise typer.Exit(0 if not errors else 1)


if __name__ == "__main__":
    cli()
