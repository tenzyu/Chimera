from datetime import datetime, timezone

from const import ID_CH_INDEX, ID_GUILD
from discord import Embed, TextChannel
from discord.ext.commands import Bot, Cog


class ChannelIndex(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.ignore_categories = [816030924872613888]
        self.title_index = "𝐓𝐨𝐩𝐢𝐜 𝐨𝐟 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬"

    @Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(ID_GUILD)
        self.ch_index = self.bot.get_channel(ID_CH_INDEX)

    async def find_index(self):
        async for m in self.ch_index.history().filter(
            lambda m: m.author == self.bot.user and m.embeds
        ):
            for e in m.embeds:
                if e.title == self.title_index:
                    return m
        return None

    def sorted_channels(self):
        return sorted(
            (
                c
                for c in self.guild.channels
                if (
                    isinstance(c, TextChannel)
                    and not c.category.id in self.ignore_categories
                )
            ),
            key=lambda c: c.position,
        )

    def create_index(self):
        e = Embed(
            title=self.title_index,
            description="\n\n".join(
                [f"━　{c.mention}\n{c.topic}" for c in self.sorted_channels()]
            ),
            timestamp=datetime.now(tz=timezone.utc),
        )
        e.set_footer(text=self.guild.name)
        return e

    async def update_index(self):
        i = await self.find_index()
        e = self.create_index()
        await i.edit(embed=e) if i else await self.ch_index.send(embed=e)

    @Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if isinstance(after, TextChannel):
            await self.update_index()


def setup(bot: Bot):
    bot.add_cog(ChannelIndex(bot))
