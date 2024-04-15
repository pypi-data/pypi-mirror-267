
import platform
import click
from keyrings.cryptfile import cryptfile
import os
import pymasscode

from sprinko.utils import check_is_installed, get_mod_hash, hashfile

def install_masscode(force_web):
    if force_web:
        import webbrowser
        return webbrowser.open("https://masscode.io/")

    # check if scoop is installed
    if platform.system() == "Windows" and check_is_installed("scoop"):
        os.system("scoop install masscode")
        
    else:
        # open website https://masscode.io/
        import webbrowser
        webbrowser.open("https://masscode.io/")

@click.command("setup")
@click.option("--force-not-found", "-fnf", is_flag=True, help="Force not found.")
@click.option("--force-web", "-fw", is_flag=True, help="Force web.")
def setup_sprinko(force_not_found, force_web):
    
    try:
        if force_not_found:
            raise
        pymasscode.Loader.currentLoader
    except: #noqa

        click.echo("Cannot find masscode installation.")
        installWish = click.prompt("Do you want to install it?", type=click.Choice(["y", "n"]), default="n")
        if not installWish:
            click.echo("If not, please manually install masscode and runs it at least once.")
            exit()

        install_masscode(force_web)
        click.prompt("Please run it once and then press Enter to continue.")

    if os.path.exists(os.path.join(os.path.dirname(pymasscode.Loader.currentLoader.dbPath), "sprinko")):
        click.echo("Sprinko is already setup, please manually delete the store file before re-init")
        os.startfile(os.path.dirname(pymasscode.Loader.currentLoader.dbPath))
        exit()

    if click.prompt("This is going to setup Sprinko. Continue?", type=click.Choice(["y", "n"]), default="n") != "y":
        return click.echo("Setup aborted")

    pwd = click.prompt("Enter a password", confirmation_prompt=True, hide_input=True)
    keyring = cryptfile.CryptFileKeyring()
    keyring.file_path = os.path.join(os.path.dirname(pymasscode.Loader.currentLoader.dbPath), "sprinko")
    keyring.keyring_key = pwd

    keyring.set_password("whole_file_hash", os.getlogin(), hashfile(pymasscode.Loader.currentLoader.dbPath))
    keyring.set_password("mod_hash", os.getlogin(), get_mod_hash())
    click.echo("Setup complete")

