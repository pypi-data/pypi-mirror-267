import typer

from rich import print

app = typer.Typer(no_args_is_help=True)

@app.callback()
def callback():
    """
    Awesome Portal Gun
    """

@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    print("[dark_green]Shooting portal gun")

@app.command()
def load():
    """
    Load the portal gun
    """
    print("[dark_goldenrod]Loading portal gun")
