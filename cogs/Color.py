import discord
from discord.ext import commands, tasks
import asyncio
from colorsys import hls_to_rgb
from discord.utils import get


class Color(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.lock = asyncio.Lock()
        self.validate = False
        self.role_name: discord.User

    async def colors(self):
        hue = 0
        for i in range(50):
            hue = (hue + 7) % 360
            rgb = [int(x * 255) for x in hls_to_rgb(hue / 360, 0.5, 1)]
            await asyncio.sleep(1 / 2)
            clr = discord.Colour(((rgb[0] << 16) + (rgb[1] << 8) + rgb[2]))
            await self.role_name.edit(colour=clr)

    @commands.command()
    async def start(self, ctx, role_name):
        guild = self.client.get_guild(689495182609219700)
        self.validate = True
        self.role_name = get(guild.roles, name=role_name)
        await self.checker.start()

    @tasks.loop(seconds=26)
    async def checker(self):
        if self.validate:
            async with self.lock:
                await self.colors()

    @commands.command()
    async def stop(self, ctx):
        self.validate = False
        self.checker.stop()
        await ctx.author.send("Функция 'rainbow nick' отключена!")


def setup(client):
    client.add_cog(Color(client))
