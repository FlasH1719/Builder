import hikari
from enum import Enum
from lightbulb import Context as _Context

__all__ = ("TranslationType", "Context")

class TranslationType(Enum):
    Message = 1
    Edit = 2
    Embed = 3

class Context(_Context):
    __slots__ = ()

    def translate_message(self, t_type: TranslationType, num: int) -> str:
        """
        Get the translated message for a server

        Params:
            t_type (TranslationType): The type of translation (Message, Edit, Embed)
            num (int): The translated message that should be used
        """

        command = ".".join(
            self.command.qualified_name.split()
        )

        transled_message = self.bot.translations["en"][command][t_type.name][str(num)]

        return transled_message