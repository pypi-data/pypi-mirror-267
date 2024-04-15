from dataclasses import dataclass, field
import os
from typing import Optional
import typing
import pymasscode
from keyrings.cryptfile import cryptfile
from pymasscode import Snippet
@dataclass(slots=True)
class Ctx:
    loader : pymasscode.Loader
    skipSecurity : bool
    keyring : Optional[cryptfile.CryptFileKeyring] = None
    gathered : typing.List[typing.Tuple[int, Snippet]] = field(default_factory=list)

    @property
    def storeFolder(self):
        return os.path.dirname(self.loader.dbPath)
    
    @property
    def storeFile(self):
        return os.path.join(self.storeFolder, "sprinko")

