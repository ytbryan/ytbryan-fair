import typer
import random
from pathlib import Path
from typing import List

app = typer.Typer()

# Path to the file that stores the order of names
REPO_PATH = Path(".")
NAMES_FILE = REPO_PATH / "names_order.txt"
TURN_FILE = REPO_PATH / "current_turn.txt"


def load_names() -> List[str]:
    if NAMES_FILE.exists():
        with open(NAMES_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []


def save_names(names: List[str]):
    with open(NAMES_FILE, "w") as f:
        for name in names:
            f.write(f"{name}\n")


def load_turns() -> List[str]:
    if TURN_FILE.exists():
        with open(TURN_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []


def save_turns(turns: List[str]):
    with open(TURN_FILE, "w") as f:
        for turn in turns:
            f.write(f"{turn}\n")


def roll_names(names: List[str]):
    # Ensure the current list of names isn't empty
    if not names:
        typer.echo("No names available.")
        return None

    # Load the current turn
    current_turn = load_turns()

    # If the current turn is complete, reset it
    if len(current_turn) == len(names):
        current_turn = []
        save_turns(current_turn)

    # Filter names to exclude those already selected in the current turn
    filtered_names = [name for name in names if name not in current_turn]

    if not filtered_names:
        return None

    # Randomly select a name from the filtered list
    selected_name = random.choice(filtered_names)
    current_turn.append(selected_name)

    # Save the updated turn
    save_turns(current_turn)

    return selected_name


@app.command()
def add(name: str):
    """
    Add a new name to the list.
    """
    names = load_names()
    if name not in names:
        names.append(name)
        save_names(names)
        typer.echo(f"Added: {name}")
    else:
        typer.echo(f"{name} is already in the list.")


@app.command()
def roll():
    """
    Roll the names and select the next one fairly.
    """
    names = load_names()
    selected_name = roll_names(names)
    if selected_name:
        typer.echo(f"Selected: {selected_name}")
    else:
        typer.echo("No names available for selection.")


@app.command()
def reset():
    """
    Reset the current turn.
    """
    TURN_FILE.unlink(missing_ok=True)
    typer.echo("Current turn has been reset.")


if __name__ == "__main__":
    app()
