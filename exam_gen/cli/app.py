from typing import Annotated, Literal
from pathlib import Path

import typer
from typer import Typer, Argument, Exit, Option
from rich import print

from ..enums import Topic

app = typer.Typer()


def _topics() -> list[str]:
    """Lists ``Topic`` enum values."""
    return [topic.value for topic in Topic]


@app.command()
def gen(
        path: Annotated[Path, Argument()] = Path('./exam.html'),
        topics: Annotated[list[str], Option()] = _topics(),
        q_amount: Annotated[int, Option()] = 10
):
    # check the values provided if not default is provided
    if set(topics) != set(_topics()):
        for topic in topics:
            if topic not in _topics():
                print(
                    f'[bold red]Irrelevant topic value provided: `{topic}`[/bold red].\nPossible values are: {_topics()}.')
                raise Exit(-1)


if __name__ == '__main__':
    app()
