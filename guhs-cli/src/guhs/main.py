#!/usr/bin/env python
import typer

from guhs import guhs_cli
from guhs.guhs_configuration import GuhsParameters


app = typer.Typer()


@app.command()
def install():
    """
    Installs GUHS in the system
    """
    guhs_cli.install()


@app.command()
def show():
    """
    Shows current configuration
    """
    guhs_cli.show()


@app.command()
def ls():
    """
    Shows boot targets
    """
    guhs_cli.ls()


@app.command()
def set(parameter: GuhsParameters, value: str):
    """
    Sets parameter
    """
    guhs_cli.set(parameter, value)


@app.command()
def get(parameter: GuhsParameters):
    """
    Gets parameter
    """
    guhs_cli.get(parameter)


@app.command()
def uninstall():
    """
    Uninstall GUHS from the system
    """
    guhs_cli.uninstall()


def main():
    app()


if __name__ == '__main__':
    main()
