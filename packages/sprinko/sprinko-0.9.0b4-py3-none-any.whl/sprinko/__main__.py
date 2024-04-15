import logging
import os
import sys
import click
import pymasscode
from keyrings.cryptfile import cryptfile
from sprinko.cmds.generate import sprinko_generate
from sprinko.cmds.run import sprinko_run
from sprinko.cmds.setup import setup_sprinko
from sprinko.core.ctx import Ctx
from sprinko.utils import get_mod_hash, hashfile, os_keyring
import sprinko.cmds.info as info

@click.group(invoke_without_command=True)
@click.option("--debug", is_flag=True, help="Enable debug mode.")
@click.option("--skip-security", "-s", is_flag=True, help="Skip security checks.")
@click.option("--password", "-p", help="Password.")
@click.pass_context
def sprinko(
    ctx: click.Context, 
    debug : bool = False,
    skip_security : bool = False,
    password : str = None
):
    click.echo("Current Mod hash: " + get_mod_hash(), color="blue")

    if debug:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    try:
        loader = pymasscode.Loader.currentLoader
        loader_success = True
    except: #noqa
        loader_success = False

    if ctx.invoked_subcommand == "setup":
        return
    
    if not loader_success:
        click.echo("Masscode is not configured correctly.")
        click.echo("Make sure you have run masscode at least once.")
        click.echo("You may use `sprinko setup` to setup Sprinko and masscode.")
        exit()

    if not os.path.exists(os.path.join(os.path.dirname(loader.dbPath), "sprinko")):
        click.echo("Sprinko is not setup.")
        click.echo("You may use `sprinko setup` to setup Sprinko.")
        exit()

    if not ctx.invoked_subcommand:
        click.echo(ctx.get_help())
    
    if ctx.invoked_subcommand in info.cmdlist:
        skip_security = True
    
    if not skip_security:
        keyring = cryptfile.CryptFileKeyring()
        keyring.file_path = os.path.join(os.path.dirname(loader.dbPath), "sprinko")
        if not password and "SPRINKO_ACCESS" in os.environ:
            password = os.environ["SPRINKO_ACCESS"]
        elif not password and (temp := os_keyring().get_password("__sprinko__", os.getlogin())):
            password = temp
        elif not password:
            password = click.prompt("Enter your password", hide_input=True)
        keyring.keyring_key = password

        # check module
        
        if keyring.get_password("mod_hash", os.getlogin()) != get_mod_hash():
            npass = click.prompt("Module has changed.", prompt_suffix="Enter your password again to continue", hide_input=True)
            if not npass == password:
                click.echo("Passwords do not match.", color="red")
                exit()
        
            keyring.set_password("mod_hash", os.getlogin(), get_mod_hash())

        if keyring.get_password("whole_file_hash", os.getlogin()) != hashfile(loader.dbPath):
            input("Masscode Database has changed.")
            keyring.set_password("whole_file_hash", os.getlogin(), hashfile(loader.dbPath))
        
    else:
        keyring = None

    ctx.obj = Ctx(loader=loader, skipSecurity=skip_security, keyring=keyring)

sprinko.add_command(setup_sprinko)
sprinko.add_command(info.version)
sprinko.add_command(info.which)
sprinko.add_command(sprinko_run)
sprinko.add_command(sprinko_generate)

def run():
    sprinko()

if __name__ == "__main__":
    run()