from pathlib import Path
from traceback import print_exc

from discord import Intents
from discord.ext.commands import Bot, when_mentioned_or

from const import DISCORD_BOT_TOKEN


class MyBot(Bot):
    def __init__(self):
        super().__init__(
            command_prefix=when_mentioned_or("!"),
            intents=Intents.all(),
        )
        print("Launching Chimera")

        for cog in Path("cogs/").glob("*.py"):
            try:
                self.load_extension(f"cogs.{cog.stem}")
                print(f"Loaded Extension:{cog.stem}")
            except Exception:
                print_exc()

    async def on_ready(self):
        print(f"logged in as: {self.user}")


if __name__ == "__main__":
    bot = MyBot()
    bot.run(DISCORD_BOT_TOKEN)
