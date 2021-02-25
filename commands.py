import discord
from discord.ext import commands
import os
import config


client = commands.Bot(command_prefix='!')
client.remove_command('help')


def is_owner():
    async def predicate(ctx):
        return 'ADMIN' in str(ctx.author.roles)
    return commands.check(predicate)


def is_all():
    async def predicate(ctx):
        return 'Учитель' or 'ADMIN' in str(ctx.author.roles)
    return commands.check(predicate)


@client.command()
@is_owner()
async def users(ctx):
    await ctx.channel.send(f"""Количество участников: {client.get_guild(config.server_id).member_count}""")


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(config.TOKEN, bot=True)
