import discord
from discord.ext import commands
import config
from discord.utils import get


class Listener(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.message) -> None:

        #  Удаление мата

        msg = message.content.lower()

        if any(bad_word in msg for bad_word in config.explicit):
            await message.channel.send(f"{message.author.mention}, следите за языком!")
            await message.delete()

        # Quiz channels

        if message.channel.id == 701183055611822201:
            await message.delete()

        if message.channel.id == 701183459040952461:
            await message.delete()

        #  Аутентификация

        if message.channel.id == 690325041128407249:
            print(str(message.content))
            await message.delete()
            if str(message.content) == '#admincontrol2020':
                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name='ADMIN'))

            try:
                name, surname, role = str(message.content).split(' ')
                if role.lower() == 'учитель':
                    new_nick = name.title() + ' ' + surname.title()
                    print(new_nick)
                    await message.author.edit(nick=new_nick)
                    await message.author.remove_roles(get(message.author.guild.roles, name='Новичок'))
                    await message.author.add_roles(get(message.author.guild.roles, name=role.title()))

                else:
                    new_role = role.lower() + ' ' + 'класс'
                    new_nick = name.title() + ' ' + surname.title()
                    print(f'Nick: {new_nick} ---- {message.author}')
                    print(f'Role: {new_role} ---- {message.author}')
                    role = get(message.author.guild.roles, name=new_role)
                    await message.author.add_roles(role)
                    await message.author.edit(nick=new_nick)
                    await message.author.send('''**У кого не работает микрофон:**
    **---С телефона---**
    `1 - нажимаем на 3 черточки в левом верхнем углу
    2 - После, в левом углу, находим свою аватарку и нажимаем
    3 - В меню ищем пункт "Голос"
    4 - В графе "ввод" выбираем "Режим рации"`
    **---С компьютера---**
    `1 - Нажать на шестеренку в левом нижнем углу
    2 - Выбираем пункт голос и видео
    3 - В графе "Режим ввода" выбираем "Режим рации"
    4 - Назначаем кнопку`
                                                Ниже правила сервера: ''', embed=config.emb())
                    await message.author.remove_roles(get(message.author.guild.roles, name='Новичок'))

            except AttributeError as e:
                print(e)
                await message.author.send('''Вы ошиблись при регистрации.
    Проверьте соответствие вашего сообщения и примера!
    вот список возможных ошибок:
    1 - Номер и буква класса написаны раздельно
    2 - Номер и буква класса написаны в кавычках''')
                print(f'AttributeError: {message.author} --- {message.content}')

            except IndexError as e:
                print(e)

                await message.author.send('''Вы ошиблись при регистрации.
    Проверьте соответствие вашего сообщения и примера!
    вот список возможных ошибок:
    1 - Номер и буква класса написаны раздельно
    2 - Номер и буква класса написаны в кавычках''')
                print(f'IndexError: {message.author} --- {message.content}')

        try:
            await self.client.process_commands(self, message)
        except TypeError:
            pass

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        role = get(member.guild.roles, name='Новичок')
        await member.add_roles(role)
        print(f'{member} зашел на сервер!')

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        sm = after.nick
        if sm:
            if sm.lower().count('helper') > 0:
                last = before.nick
                if last:
                    await after.edit(nick=last)
                else:
                    await after.edit(nick="DON'T DO THAT!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} покинул сервер!')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('Commands: !help'))
        print(f'Бот в сети {self.client.user}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send('Пожалуйста, введите все аргументы команды')


def setup(client):
    client.add_cog(Listener(client))
