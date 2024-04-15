from functools import cache
import subprocess
import platform
import os
import typing


def check_is_installed(app_name):
    """
    Check if an application is installed on the operating system.
    
    Args:
    app_name (str): The name of the application to check.
    
    Returns:
    bool: True if the application is installed, False otherwise.
    """
    os_type = platform.system()

    try:
        if os_type == 'Windows':
            # On Windows, use 'where' command to check for the app existence
            subprocess.check_call(['where', app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_type == 'Darwin':
            # On macOS, use 'type' command or 'which'
            subprocess.check_call(['type', app_name], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_type == 'Linux':
            # On Linux, use 'which' command
            subprocess.check_call(['which', app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            return False
    except subprocess.CalledProcessError:
        # The command failed, the application is not installed
        return False

    # The command succeeded, the application is installed
    return True

def hashfile(path):
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def hashfolder(path, extensions : typing.List[str] = [".py"]):
    import hashlib
    sha256_hash = hashlib.sha256()

    for root, _, files in os.walk(path):
        for file in files:
            if extensions and not file.endswith(tuple(extensions)):
                continue
        
            with open(os.path.join(root, file), "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@cache
def get_mod_hash():
    from .. import __thisdir__
    return hashfolder(
        __thisdir__,
    )


@cache
def os_keyring(spec : str = None):
    if spec == "kwallet":
        from keyring.backends.kwallet import DBusKeyring
        return DBusKeyring()
    if platform.system() == "Windows":
        from keyring.backends.Windows import WinVaultKeyring
        return WinVaultKeyring()
    elif platform.system() == "Darwin":
        from keyring.backends.macOS import Keyring
        return Keyring()
    elif platform.system() == "Linux":
        from keyring.backends.SecretService import Keyring
        return Keyring()