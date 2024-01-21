from pathlib import Path

import click.types
from click import group, command, echo, argument, pass_context

from rag_diary.boot import boot
from rag_diary.config import Config
from rag_diary.entry import EntryHandler


@group()
@pass_context
def cli(ctx, *args, **kwargs):
    entry_handler = boot(Config())
    ctx.obj = {"entry_handler": entry_handler}


@command()
def hello():
    """This command prints 'Hello, World!'"""
    echo("Hello, World!")


@command()
@argument("entry")
@pass_context
def new_entry(ctx, entry):
    entry_handler: EntryHandler = ctx.obj.get("entry_handler")
    entry_handler.add_entry(entry)

@command()
@click.argument("entry", type=click.Path(exists=True))
@pass_context
def new_entry_file(ctx, entry: Path):
    entry_handler: EntryHandler = ctx.obj.get("entry_handler")
    entry_handler.add_new_entry_from_file(entry)


cli.add_command(hello)
cli.add_command(new_entry)

if __name__ == "__main__":
    cli()
