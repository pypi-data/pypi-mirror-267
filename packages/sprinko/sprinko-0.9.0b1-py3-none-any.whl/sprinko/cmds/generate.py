
import click
import sprinko.cmds._query as query
from sprinko.core import resolve_snippet
from sprinko.core.ctx import Ctx

@click.group("generate", invoke_without_command=True, chain=True, short_help="Generate output")
@click.option("--id", "-i", help="Run by ID")
@click.option("--name", "-n", help="Run by exact name")
@click.option("--frag", "-f", help="Run fragment index", type=click.INT, default=0)
@click.option("--out", "-o", type=click.STRING, help="Output file", default="output")
# custom
@click.pass_context
def sprinko_generate(ctx : click.Context, id : str = None, name : str = None, frag : int = 0 , save : str = None, live_eval : bool = False):
    tsnippet = resolve_snippet(ctx, id, name)
    if tsnippet:
        ctx.obj.gathered.append((frag, tsnippet))

@sprinko_generate.result_callback()
@click.pass_obj
def sprinko_run_result(obj : Ctx, *args, **kwargs):
    save = kwargs.get("save", None)
    if save:
        # currently unsupported
        click.echo("Saving is not yet supported", color="red")
    
    with open(kwargs.get("out", "output"), "w") as f:
        for (frag, gather) in obj.gathered:
            f.write(gather.content[frag]["value"])

sprinko_generate.add_command(query.qry)
sprinko_generate.add_command(query.query)
sprinko_generate.add_command(query.qname)
sprinko_generate.add_command(query.qid)