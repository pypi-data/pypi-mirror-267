
import click
from pymasscode import Snippet
from sprinko.core import queryid
from sprinko.core.ctx import Ctx
from sprinko.core.mselect import MasscodeSelection

def _query(obj : Ctx, var : str, frag : int = 0):
    res = Snippet.queryParse(var)
    if len(res) == 0:
        click.echo("No results found")
        exit()

    if len(res) == 1:
        obj.gathered.append((frag, res[0]))

    if len(res) > 1:
        mse = MasscodeSelection(res)
        mse.run()
        obj.gathered.append((frag, mse.selected))


@click.command("query")
@click.argument("var")
@click.option("--frag", "-f", help="Fragment index", type=click.INT, default=0)
@click.pass_obj
def query(obj : Ctx, var :str, frag : int = 0):
    return _query(obj,var, frag)

@click.command()
@click.argument("var")
@click.option("--frag", "-f", help="Fragment index", type=click.INT, default=0)
@click.pass_obj
def qry(obj : Ctx, var :str, frag : int = 0):
    return _query(obj,var, frag)

@click.command()
@click.argument("var")
@click.option("--frag", "-f", help="Fragment index", type=click.INT, default=0)
@click.pass_obj
def qid(obj : Ctx, var :str, frag : int = 0):
    res = queryid(var)
    if len(res) == 0:
        click.echo("No results found")
        exit()

    if len(res) == 1:
        obj.gathered.append((frag, res[0]))


@click.command()
@click.argument("var")
@click.option("--frag", "-f", help="Fragment index", type=click.INT, default=0)
@click.pass_obj
def qname(obj : Ctx, var :str, frag : int = 0):
    res = queryid(var)
    if len(res) == 0:
        click.echo("No results found")
        exit()

    if len(res) == 1:
        obj.gathered.append((frag, res[0]))

    if len(res) > 1:
        mse = MasscodeSelection(res)
        mse.run()
        obj.gathered.append((frag, mse.selected))