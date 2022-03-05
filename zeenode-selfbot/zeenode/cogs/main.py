import discord, requests, pyfiglet, datetime, aiohttp, urllib3, asyncio
import io
from discord.ext import commands as zeenode
from zeenode.load import token
from zeenode.config import prefix

bot = zeenode.Bot(command_prefix=prefix, self_bot=True)
bot.remove_command("help")

Output = "[ERROR] - "


class Main(zeenode.Cog):
    def __init__(self, bot):
        self.bot = bot

    @zeenode.command()
    async def ascii(self, ctx, args):
        await ctx.message.delete()
        text = pyfiglet.figlet_format(args)
        await ctx.send(f"```{text}```")

    @zeenode.command()
    async def hypesquad(self, ctx, house):
        await ctx.message.delete()
        request = requests.session()
        headers = {"Authorization": token, "Content-Type": "application/json"}

        global payload

        if house == "bravery":
            payload = {"house_id": 1}
        elif house == "brilliance":
            payload = {"house_id": 2}
        elif house == "balance":
            payload = {"house_id": 3}

        try:
            requests.post(
                "https://discordapp.com/api/v6/hypesquad/online",
                headers=headers,
                json=payload,
            )
            print(f"{Fore.GREEN} Succesfully set your HypeSquad house to {house}!")
        except:
            print(
                f"{Fore.RED}{Output} {Fore.YELLOW}Failed to set your HypeSquad house to {house}."
            )

    @zeenode.command()
    async def help(self, ctx, category=None):
        await ctx.message.delete()
        if category is None:
            await ctx.send(
                """```fix
Activity           - Shows all activity
Currency           - Shows all currency
Emoticons          - Shows all emoticons
Fun                - Shows all fun
Main               - Shows all main
Mass               - Shows all mass
Nsfw               - Shows all nsfw
TextEncoding       - Shows all textencoding
```"""
            )
        elif str(category).lower() == "activity":
            await ctx.send(
                """```fix
Activity Commands\n> listening <text> - Shows listening status.\n> playing <text> - Shows playing status.\n> watching <text> - Shows watching status.\n> streaming <text> - Shows streaming status.\n> stopactivity - Stops activity.
```"""
            )

        elif str(category).lower() == "currency":
            await ctx.send(
                """```fix
Currency Commands\n> btc - Shows Bitcoin price. \n> doge - Shows Doge price.\n> eth - Shows Ethereum price.\n> xmr - Shows Monero price.\n> xrp - Shows Ripple price.
```"""
            )
        elif str(category).lower() == "emoticons":
            await ctx.send(
                """```fix
Emoticons Commands\n> fuckyou - Sends fuckyou emoticon. \n> lenny - Sends lenny emoticon.\n> what - Sends what emoticon.\n> bear - Sends bear emoticon.\n> worried - Sends worried emoticon.\n> ak47 - Sends ak47 emoticon.\n> awp - Sends awp emoticon.\n> lmg - Sends lmg emoticon.\n> sword - Sends sword emoticon.\n> love - Sends love emoticon.\n> goodnight - Sends goodnight emoticon.\n> smile - Sends smile emoticon.
```"""
            )
        elif str(category).lower() == "fun":
            await ctx.send(
                """```fix
Fun Commands\n> cat - Sends a random cat image.\n> dog - Sends a random dog image.\n> panda - Sends a random panda image.\n> dick <@user> - Shows user dick size.\n> hug <@user> - Sends a hug to user.\n> kiss <@user> - Sends a kiss to user.\n> slap <@user> - Sends a slap to user.\n> meme - Sends a random meme.\n> nitro - Sends a nitro.
```"""
            )
        elif str(category).lower() == "main":
            await ctx.send(
                """```fix
Main Commands\n> ascii <message> - Sends message as ascii art. \n> av <@user> - Sends your avatar in the chat.\n> guildicon - Shows server (guild) icon.\n> serverinfo - Shows server info.\n> whois <@user> - Sends info about user.\n> hypesquad <house> - Allows you to change your hypesquad house/badge.\n> purge <number of messages> - Deletes messages.\n> suggest <question> - Sends question with embed leaving thumbsup & thumbsdown react.
```"""
            )
        elif str(category).lower() == "mass":
            await ctx.send(
                """```fix
Mass Commands\n> massreact <emoji> - Reacts to last 20 messages with emojis.\n> spam <number of messages> <message>  - Spams messages\n> msgedit <edit_to>.
```"""
            )
        elif str(category).lower() == "nsfw":
            await ctx.send(
                """```fix
Nsfw Commands\n> anal <user> - Sends nsfw anime content.\n> blowjob <user> - Sends nsfw anime content.\n> boobs <user> - Sends nsfw anime content.\n> hentai <user> - Sends hentai (anime porn).
```"""
            )
        elif str(category).lower() == "textencoding":
            await ctx.send(
                """```fix
Text Encoding Commands\n> encode_base64 <word/message> - Encodes text with Base64.\n> decode_base64 <word/message> - Decodes Base64 text\n> encode_leet <word/message> - Encodes text with leet speak.\n> encode_md5 <word/message> - Encodes text with MD5 hash.\n> encode_sha1 <word/message> - Encodes text with Sha1.\n> encode_sha224 <word/message> - Encodes text wish SHA224.\n> encode_sha384 <word/message> - Encodes text with Sha384.\n> encode_sha251 <word/message> - Encodes text with Sha512.
```"""
            )

    @zeenode.command(aliases=["suggestion"])
    async def suggest(self, ctx, *, suggestion):
        await ctx.message.delete()
        msg = await ctx.send(suggestion)
        await msg.add_reaction("\U0001F44D")
        await msg.add_reaction("\U0001F44E")

    @zeenode.command(aliases=["pfp", "avatar"])
    async def av(self, ctx, *, user: discord.User = None):
        await ctx.message.delete()
        format = "gif"
        user = user or ctx.author
        if user.is_avatar_animated() != True:
            format = "png"
        avatar = user.avatar_url_as(format=format if format != "gif" else None)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar)) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"Avatar.{format}"))

    @zeenode.command(aliases=["guildinfo"])
    async def serverinfo(self, ctx):
        await ctx.message.delete()
        date_format = "%a, %d %b %Y %I:%M %p"
        await ctx.send(
            f"""```Server Info of {ctx.guild.name}:
{ctx.guild.member_count} Members\n {len(ctx.guild.roles)} Roles\n {len(ctx.guild.text_channels)} Text-Channels\n {len(ctx.guild.voice_channels)} Voice-Channels\n {len(ctx.guild.categories)} Categories,
Server created at, {ctx.guild.created_at.strftime(date_format)}
Server Owner, <@{ctx.guild.owner_id}>
Server ID, {ctx.guild.id}
url={ctx.guild.icon_url}```"""
        )

    @zeenode.command()
    async def guildicon(self, ctx):
        await ctx.message.delete()
        await ctx.send(ctx.guild.icon_url)

    @zeenode.command()
    async def whois(self, ctx, *, user: discord.User = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        return await ctx.send(
            (
                f"""
{user.mention}
{(user), user.avatar_url}
{user.avatar_url}
"Registered", {user.created_at.strftime(date_format)}
"""
            )
        )


def setup(bot):
    bot.add_cog(Main(bot))
