
import os
import typing
from sprinko.utils.selection import Selection
from pymasscode import Snippet

class MasscodeSelection(Selection):
    def __init__(self, snippets : typing.List[Snippet], index=0):
        options = {s.name : s.id for s in snippets}
        self.__snippets = snippets
        super().__init__(options, index)

    def daction(self):
        os.startfile(f"masscode://snippets/{self.options[self.__index]}")

    @property
    def selected(self):
        return self.__snippets[self.__index]