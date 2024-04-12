import typer
from rich import print
from typing_extensions import Annotated
from pathlib import Path
from termcolor import cprint

from ryax.ryax_metadata.ryax_metadata import RyaxMetadata
from ryax.utils.check import discover_action_dirs

octopus_emoji = "\U0001F419"
app = typer.Typer()


@app.command()
def init(
    to_dir: Annotated[
        Path,
        typer.Argument(
            help="Directory in which a new ryax development project will be created."
        ),
    ] = Path.cwd()
):
    if Path(to_dir / ".ryax").exists():
        cprint(
            "Error: ",
            "red",
            attrs=["bold"],
            end=f"Found existing ryax project at {to_dir.absolute()}\n",
        )
        return
    new_project = Path(to_dir).absolute()
    new_project.mkdir(exist_ok=True)
    ryax_cache_dir = new_project / ".ryax"
    ryax_cache_dir.mkdir(exist_ok=False)
    Path(new_project / "actions").mkdir(exist_ok=True)
    print(f"{octopus_emoji} Created new ryax project at: {new_project}")


@app.command()
def check(
    force: Annotated[bool, typer.Option("--force", "-f")] = False,
    to_dir: Annotated[
        Path,
        typer.Argument(help="Directory to check."),
    ] = Path.cwd(),
):
    action_dirs = discover_action_dirs(to_dir)
    print(f"Collected {len(action_dirs)} actions to analyse.")
    for action_dir in action_dirs:
        action_metadata = (
            RyaxMetadata.from_metadata_and_handler_file(action_dir)
            if Path(action_dir / "ryax_metadata.yaml").is_file()
            else RyaxMetadata.from_handler_file(action_dir)
        )
        if force and action_metadata.generated_metadata:
            action_metadata.write_metadata()
        elif not force and action_metadata.generated_metadata:
            print(
                f"Found an action with no metadata et {action_metadata.action_dir}. Use -f to autogenerate."
            )
        action_metadata.check_action_data()
        if len(action_metadata.scan_errors) == 0:
            print(f"{action_metadata.action_dir} OK!")
        else:
            print(
                f"Analysis of action at {action_metadata.action_dir} failed with error {action_metadata.scan_errors}"
            )
    print(f"{octopus_emoji} Done")


def main() -> None:
    app()


if __name__ == "__main__":
    app()
