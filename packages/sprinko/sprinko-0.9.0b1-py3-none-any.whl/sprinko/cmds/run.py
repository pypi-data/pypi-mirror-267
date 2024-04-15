
import click
import sprinko.cmds._query as query
from sprinko.core import getEnv, resolve_snippet, run_snippet
from sprinko.core.ctx import Ctx
import ptpython

@click.group("run", invoke_without_command=True, chain=True)
@click.option("--id", "-i", help="Run by ID")
@click.option("--name", "-n", help="Run by exact name")
@click.option("--frag", "-f", help="Run fragment index", type=click.INT, default=0)
@click.option("--save", "-s", type=click.STRING, help="Save as profile")
# custom
@click.option("--live-eval", "-l", is_flag=True, help="Live eval")
@click.pass_context
def sprinko_run(ctx : click.Context, id : str = None, name : str = None, frag : int = 0 , save : str = None, live_eval : bool = False):
    tsnippet = resolve_snippet(ctx, id, name)
    if tsnippet:
        ctx.obj.gathered.append((frag, tsnippet))

@sprinko_run.result_callback()
@click.pass_obj
def sprinko_run_result(obj : Ctx, *args, **kwargs):
    save = kwargs.get("save", None)
    if save:
        # currently unsupported
        click.echo("Saving is not yet supported", color="red")
    
    for (frag, gather) in obj.gathered:
        run_snippet(gather, frag)

    if kwargs.get("live_eval", False):
        ptpython.repl.embed(getEnv())

sprinko_run.add_command(query.qry)
sprinko_run.add_command(query.query)
sprinko_run.add_command(query.qname)
sprinko_run.add_command(query.qid)