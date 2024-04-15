

from functools import cache
import click
from pymasscode import Snippet
from sprinko.core.mselect import MasscodeSelection
import sprinko.utils.std as std

__run_environment = {}

@cache
def getEnv():
    global __run_environment
    # populate everything in std to the environment
    for k, v in std.__dict__.items():
        if k.startswith("__"):
            continue
        __run_environment[k] = v
    return __run_environment

def queryname(name :str):
    return Snippet.query(Snippet.q.name == name)

def queryid(id : str):
    return Snippet.query(Snippet.q.id == id)

def runPython(snippet :Snippet, frag : int):
    content = snippet.content[frag]
    script = content["value"]

    try:
        exec(script, getEnv())
    except ImportError as e:
        click.echo("Missing module: " + e.name, color="red")    

def run_snippet(snippet : Snippet, frag : int = 0):
    lang = snippet.content[frag]["language"]
    click.echo(f"======== {snippet.name + ' - ' + snippet.content[frag]['label']} ========", color="green")
    if lang == "python":
        runPython(snippet, frag)
    else:
        click.echo("Unsupported language: " + lang, color="red")
        exit()


def resolve_snippet(ctx : click.Context, id : str = None, name : str = None):
    if id or name:
        if ctx.invoked_subcommand is not None:
            raise click.UsageError("Cannot use --id or --name with subcommand")

        if id is not None:
            res = queryid(id)
        elif name is not None:
            res = queryname(name)
            if len(res) > 1:
                select = MasscodeSelection(res)
                select.run()
                tsnippet = select.selected
        
        if len(res) == 0:
            click.echo(f"Could not find {id or name}")
            exit()

        if len(res) == 1:
            tsnippet = res[0]

    return tsnippet