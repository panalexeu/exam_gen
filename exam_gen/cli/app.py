from typing import Annotated, Literal, get_args
from pathlib import Path

import typer
from openai import OpenAI
from openai.types import ChatModel

from typer import Typer, Argument, Exit, Option
from rich import print
from dotenv import load_dotenv

from ..enums import Topic
from ..llm import gen_exam, Exam
from ..adapters.exam_file import exam_to_html

app = typer.Typer()


def _topics() -> list[str]:
    """Lists ``Topic`` enum values."""
    return [topic.value for topic in Topic]


@app.command()
def gen(
        path: Annotated[Path, Argument()] = Path('./exam.html'),
        topics: Annotated[list[str], Option()] = _topics(),
        q_amount: Annotated[int, Option()] = 10,
        model: Annotated[str, Option()] = 'gpt-4.1-mini',
        temperature: Annotated[int, Option()] = 1
):
    # check the values provided if not default is provided
    if set(topics) != set(_topics()):
        for topic in topics:
            if topic not in _topics():
                print(
                    f'[bold red]Irrelevant topic value provided: `{topic}`[/bold red].\nPossible values are: {_topics()}.')
                raise Exit(-1)

    # check the model name value
    if model not in list(get_args(ChatModel)):
        print(
            f'[bold red]Irrelevant model name provided: `{model}`[/bold red].\nPossible values are: {ChatModel}.')
        raise Exit(-1)

    # generate an exam
    load_dotenv()
    res: Exam = gen_exam(
        topics=topics,
        q_amount=q_amount,
        client=OpenAI(),
        model=model,
        temperature=temperature
    )
    breakpoint()

    # create an exam html
    html = exam_to_html(res)
    with open(path, 'w') as file:
        file.write(html)

    print(f'Done! The exam is generated under [bold green]`{path}`[/bold green].')


if __name__ == '__main__':
    app()
