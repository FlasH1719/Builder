import time
from builder.bot import BuilderBot, Context, TranslationType
from lightbulb import Plugin, command

class Bot(Plugin):
    """
    Info about the bot and basic commands
    """

    __slots__ = ("bot", )

    def __init__(self, bot: BuilderBot) -> None:
        self.bot = bot

        super().__init__()

    @command()
    async def ping(self, ctx: Context) -> None:
        """
        Get the heartbeat and REST API latency of the bot
        """

        t_msg = ctx.translate_message(
            TranslationType.Message,
            1
        )
        start = time.perf_counter()
        message = await ctx.respond(t_msg)

        ack = round((time.perf_counter() - start) * 1000)
        heartbeat = round(self.bot.heartbeat_latency * 1000)
        t_edited_msg = ctx.translate_message(
            TranslationType.Edit,
            1
        ).format(heartbeat, ack)

        await message.edit(t_edited_msg)


def load(bot: BuilderBot) -> None:
    bot.add_plugin(Bot(bot))