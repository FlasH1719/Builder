import hikari
from enum import Enum
from typing import Union
from lightbulb import Context as _Context

__all__ = ("TranslationType", "Context")

class TranslationType(Enum):
    Text = 1
    Embed = 2

class Context(_Context):
    __slots__ = ()

    def translate_message(self, t_type: TranslationType, index: int, /) -> Union[str, hikari.Embed]:
        """
        Get the translated message for a server

        Params:
            t_type (TranslationType): The type of translation (Text, Embed)
            index (int): The translated message that should be used
        """

        command = ".".join(
            self.command.qualified_name.split()
        )

        translation = self.bot.translations["en"][command][t_type.name][index]

        if isinstance(translation, dict):
            return self.bot.entity_factory.deserialize_embed(translation)

        return translation