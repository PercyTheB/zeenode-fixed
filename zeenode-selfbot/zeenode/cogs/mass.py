import discord, pyfiglet
from discord.ext import commands as zeenode


class mass(zeenode.Cog):
    def __init__(self, bot):
        self.bot = bot

    @zeenode.command()
    async def massreact(self, ctx, emote):
        await ctx.message.delete()
        messages = await ctx.message.channel.history(limit=20).flatten()
        for message in messages:
            await message.add_reaction(emote)

    @zeenode.command()
    async def spam(self, ctx, amount: int = None, *, message: str = None):
        await ctx.message.delete()
        for each in range(0, amount):
            await ctx.send(f"{message}")

    @zeenode.command(aliases=["editall"])
    async def msgedit(self, ctx):
        await ctx.message.delete()
        edit_to = ctx.message.content[len("$") + 8 :]
        messages = await ctx.message.channel.history(limit=None).flatten()
        for message in messages:
            try:
                await message.edit(content=edit_to)
            except:
                pass
        print(f"Finished editing all messages to {edit_to}")

    @zeenode.command()
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        async for message in ctx.message.channel.history(limit=amount).filter(
            lambda m: m.author == self.bot.user
        ).map(lambda m: m):
            try:
                await message.delete()
            except:
                print(f"Purge failed")


def setup(bot):
    bot.add_cog(mass(bot))
