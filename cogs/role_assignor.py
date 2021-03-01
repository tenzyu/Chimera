from const import ID_GUILD, ID_ROLE_BOT, ID_ROLE_MEMBER
from discord import Member
from discord.ext.commands import Bot, Cog, Context, command, has_permissions


class RoleAssignor(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(ID_GUILD)
        self.role_bot = self.guild.get_role(ID_ROLE_BOT)
        self.role_member = self.guild.get_role(ID_ROLE_MEMBER)

    async def assign_role(self, m: Member):
        r = self.role_bot if m.bot else self.role_member
        if r in m.roles:
            return
        await m.add_roles(r)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await self.assign_role(member)

    @command(hidden=True)
    @has_permissions(administrator=True)
    async def refresh(self, ctx: Context):
        [await self.assign_role(member) for member in self.guild.members]
        await ctx.reply("Done.")


def setup(bot: Bot):
    bot.add_cog(RoleAssignor(bot))
