from datetime import datetime, timezone

from const import ID_CH_INDEX, ID_GUILD
from discord import Embed, TextChannel
from discord.ext.commands import Bot, Cog


class TopicIndexer(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.ignore_categories = [816030924872613888]
        self.index_embed_title = "𝐓𝐨𝐩𝐢𝐜 𝐨𝐟 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬"

    @Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(ID_GUILD)
        self.ch_index = self.bot.get_channel(ID_CH_INDEX)

    async def find_index(self):
        async for my_message_has_embed in self.ch_index.history().filter(
            lambda m: m.author == self.bot.user and m.embeds
        ):
            for embed in my_message_has_embed.embeds:
                if embed.title == self.index_embed_title:
                    return my_message_has_embed
        return None

    def index_channels(self):
        return [
            channel
            for channel in self.guild.text_channels
            if not channel.category.id in self.ignore_categories
        ]

    def index_embed_description(self):
        return "\n\n".join(
            [
                f"━　{channel.mention}\n{channel.topic}"
                for channel in self.index_channels()
            ]
        )

    def create_index_embed(self):
        embed = Embed(
            title=self.index_embed_title,
            description=self.index_embed_description(),
            timestamp=datetime.now(tz=timezone.utc),
        )
        embed.set_footer(text=self.guild.name)
        return embed

    async def update_index(self):
        index = await self.find_index()
        embed = self.create_index_embed()
        await (index.edit(embed=embed) if index else self.ch_index.send(embed=embed))

    @Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if isinstance(after, TextChannel):
            await self.update_index()


def setup(bot: Bot):
    bot.add_cog(TopicIndexer(bot))
