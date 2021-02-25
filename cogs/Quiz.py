import discord
from discord.utils import get
from discord.ext import commands
import sqlite3
from commands import is_all, is_owner


class Quiz(commands.Cog):

    def __init__(self, client):
        self.client = client

    @is_owner()
    @commands.command()
    async def db(self, ctx):
        con = sqlite3.connect('cogs/data/quiz.db')
        cur = con.cursor()
        x = cur.execute('SELECT * FROM teams')
        for i in x:
            print(i)

    @commands.command(aliases=['r'])
    async def register(self, ctx, team: str, *members: discord.Member):
        guild = ctx.guild
        con = sqlite3.connect('cogs/data/quiz.db')
        cur = con.cursor()

        if len(members) > 7:
            await ctx.author.send('Вы превысили лимит участников в команде!')

        else:
            if ctx.channel.id == 701183055611822201:
                check_role = get(guild.roles, name='Учитель').position
                answer_channel = get(guild.channels, id=701183459040952461)

                await guild.create_role(name=team)
                category = get(guild.categories, id=700701422722875534)
                await guild.create_voice_channel(name=team, category=category)
                tm = get(guild.channels, name=team)
                role = get(guild.roles, name=team)
                await tm.set_permissions(role, view_channel=True, connect=True,
                                         speak=True, use_voice_activation=True)

                await answer_channel.set_permissions(ctx.message.author, read_messages=True, send_messages=True,
                                                     read_message_history=False)

                for member in members:
                    await member.add_roles(role)
                await ctx.author.add_roles(role)

                await role.edit(position=check_role)
                await ctx.author.send(f'**Ваша команда зарегестрована!**\nВаш канал: **{team}**')

                print(f'Команада {team} зарегестрирована!')
                cur.execute(f'''INSERT INTO teams VALUES ("{team}")''')
                con.commit()

                con.close()

            else:
                await ctx.author.send('Ошиблись каналом!')

    @commands.command(aliases=['a'])
    async def answer(self, ctx, *answers):

        if ctx.channel.id == 701183459040952461:
            team = ctx.author.top_role
            teacher = get(ctx.guild.members, id=689113292337184883)
            await teacher.send(f'**Ответ команды {team}**')

            f = open('cogs/info_files/answers.txt', mode='w')
            for enum, answer in enumerate(answers):
                f.write(f'{enum + 1}. {answer}\n')
            f.close()
            f = open('cogs/info_files/answers.txt', mode='r')
            await teacher.send(f.read())
            await teacher.send('--------')

            print(f'Ответ {answers} принят!')
            f.close()
            await ctx.author.send('**Ваш ответ принят!**')

        else:
            await ctx.author.send('Проверьте канал!')

    @is_all()
    @commands.command()
    async def end(self, ctx):
        con = sqlite3.connect('cogs/data/quiz.db')
        cur = con.cursor()
        guild = ctx.guild
        channel_room = get(guild.channels, id=700708360969781348)
        answer_channel = get(guild.channels, id=701183459040952461)
        answer_channel_members = answer_channel.members

        teams = cur.execute('SELECT * FROM teams').fetchall()
        print(teams)

        for team in teams:
            channel = get(guild.channels, name=str(*team))
            role = get(guild.roles, name=str(*team))

            await role.delete()
            await channel.delete()

        for member in answer_channel_members:
            await answer_channel.set_permissions(member, overwrite=None)

        await channel_room.send('**ВИКТОРИНА ЗАКОНЧЕНА!**')
        print('Викторина закончена!')
        cur.execute('DELETE FROM teams')
        con.commit()

        await ctx.message.delete()


def setup(client):
    client.add_cog(Quiz(client))
