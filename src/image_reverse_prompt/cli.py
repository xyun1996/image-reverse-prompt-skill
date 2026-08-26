import json
from pathlib import Path

import typer

from .analyzer import analyze_image_to_schema
from .compiler import compile_from_schema
from .io_utils import dump_json
from .palette import extract_palette
from .reverse import reverse_image
from .schema_tools import validate_json_file

app = typer.Typer(help="Image Reverse Prompt CLI")


@app.command()
def palette(
    image: Path,
    colors: int = typer.Option(6, "--colors", min=2, max=16),
    as_json: bool = typer.Option(False, "--json"),
):
    result = extract_palette(image, num_colors=colors)
    if as_json:
        typer.echo(dump_json(result))
        return
    for item in result["colors"]:
        typer.echo(f'{item["hex"]}\tshare={item["share"]:.4f}')


@app.command()
def validate(
    schema_file: Path,
    schema_type: str = typer.Option("general", "--schema-type"),
):
    validate_json_file(schema_file, schema_type=schema_type)
    typer.echo("OK")


@app.command()
def analyze(
    image: Path,
    provider: str = typer.Option("openai", "--provider"),
    model: str | None = typer.Option(None, "--model"),
    schema_type: str = typer.Option("general", "--schema-type"),
    no_verify: bool = typer.Option(False, "--no-verify"),
    output: Path | None = typer.Option(None, "--output", "-o"),
):
    result = analyze_image_to_schema(image, provider, model, schema_type, verify=not no_verify)
    text = dump_json(result)
    if output:
        output.write_text(text + "\n", encoding="utf-8")
    typer.echo(text)


@app.command("compile")
def compile_cmd(
    schema_file: Path,
    target: str = typer.Option("flux", "--target"),
    provider: str = typer.Option("openai", "--provider"),
    model: str | None = typer.Option(None, "--model"),
    output: Path | None = typer.Option(None, "--output", "-o"),
):
    prompt = compile_from_schema(schema_file, target, provider, model=model)
    if output:
        output.write_text(prompt + "\n", encoding="utf-8")
    typer.echo(prompt)


@app.command()
def reverse(
    image: Path,
    target: str = typer.Option("flux", "--target"),
    provider: str = typer.Option("openai", "--provider"),
    model: str | None = typer.Option(None, "--model"),
    schema_type: str = typer.Option("general", "--schema-type"),
    colors: int = typer.Option(6, "--colors", min=2, max=16),
    no_verify: bool = typer.Option(False, "--no-verify"),
    output: Path | None = typer.Option(None, "--output", "-o"),
):
    result = reverse_image(
        image_path=image,
        target=target,
        provider_name=provider,
        model=model,
        schema_type=schema_type,
        num_colors=colors,
        verify=not no_verify,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if output:
        output.write_text(text + "\n", encoding="utf-8")
    typer.echo(text)


def main():
    app()


if __name__ == "__main__":
    main()
