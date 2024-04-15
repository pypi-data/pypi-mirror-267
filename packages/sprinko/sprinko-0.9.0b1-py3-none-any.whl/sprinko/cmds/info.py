
import click
from sprinko import __version__
from sprinko.core.ctx import Ctx

@click.command()
def version():
    click.echo(__version__)

@click.command()
@click.pass_obj
def which(obj : Ctx):
    click.echo(obj.storeFile)

cmdlist = ["version", "which"]