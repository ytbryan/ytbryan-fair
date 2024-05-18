import typer
import random
import git
from pathlib import Path
from typing import List

app = typer.Typer()

# Path to the file that stores the order of names
REPO_PATH = Path(".")
NAMES_FILE = REPO_PATH / "names_order.txt"


def commit_changes(repo, message):
    repo.index.add([str(NAMES_FILE)])
    repo.index.commit(message)


def load_names() -> List[str]:
    if NAMES_FILE.exists():
        with open(NAMES_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []


def save_names(names: List[str]):
    with open(NAMES_FILE, "w") as f:
        for name in names:
            f.write(f"{name}\n")


def roll_names(names: List[str]):
    # Ensure the current list of names isn't empty
    if not names:
        typer.echo("No names available.")
        return None

    if len(names) == 1:
        return names[0]

    # Get the last selected name to avoid selecting it again
    repo = git.Repo(REPO_PATH)
    commit_messages = [commit.message for commit in repo.iter_commits(paths=NAMES_FILE)]
    if commit_messages:
        last_selected_name = commit_messages[0].split(": ")[1].strip()
    else:
        last_selected_name = None

    # Filter names to exclude the last selected one
    filtered_names = [name for name in names if name != last_selected_name]
    
    if not filtered_names:
        return None
    
    # Randomly select a name from the filtered list
    selected_name = random.choice(filtered_names)
    names.remove(selected_name)
    names.append(selected_name)  # Move the selected name to the end of the list

    save_names(names)
    commit_changes(repo, f"Selected: {selected_name}")

    return selected_name


@app.command()
def add(name: str):
    """
    Add a new name to the list.
    """
    names = load_names()
    names.append(name)
    save_names(names)
    repo = git.Repo(REPO_PATH)
    commit_changes(repo, f"Added: {name}")
    typer.echo(f"Added: {name}")


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


if __name__ == "__main__":
    app()
