import discord
from discord.ext import commands
from random import choice, randint


class OtherCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['очистить'])
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=['отправить'])
    async def send_to(self, ctx, member: discord.Member, message=None):
        await member.send(f'{member.name}, привет от {ctx.author.name}\nMessage: {message}')
        await ctx.message.delete()

    @commands.command(aliases=['помощь'])
    async def help(self, ctx):
        emd = discord.Embed(title='Информация о доступных командах', color=15844367)
        emd.add_field(name='!дз <сообщение>', value='Сделать объявление о закреплении домашнего задания')
        emd.add_field(name='!вопрос <вопрос>', value='Можете задать вопрос нашему боту')
        emd.add_field(name='!отправить <сообщение>', value='Отправить сообщение в личку')
        emd.add_field(name='!монетка', value='Подбросить монетку')
        emd.add_field(name="!следурок <класс>",
                      value="Узнать следующий урок для конкретного класса. Оставьте поле пустым, "
                      "чтобы вывести ближайший урок.",
                      inline=True)
        emd.add_field(name="!добавитьурок <дд.мм> <чч:мм> <класс> <тема и предмет>",
                      value="Добавить урок в расписание.",
                      inline=False)
        emd.add_field(name="!расписание <класс>", value="Показывает расписание для класса/всех классов.", inline=True)
        emd.add_field(name="!кдоске", value="Вызывает случайного ученика к доске")
        emd.add_field(name="!ученики", value="Список присутствующих на уроке")
        emd.add_field(name='!статьи', value="Найдите статью по душе!")
        emd.set_footer(text=f"Вызвано: {ctx.author.name}")
        await ctx.author.send('Check this!', embed=emd)
        await ctx.message.delete()

    @commands.command(aliases=['вопрос'])
    async def _8ball(self, ctx, *, question):
        responses = ['Это точно',
                     'Так, решено!',
                     'Да, безусловно',
                     'Вы можете положиться на него',
                     'Как я понимаю, да',
                     'Вполе вероятно',
                     'Выглядить неплохо',
                     'Да',
                     'Непонятный ответ, попробуйте еще раз!',
                     'Спросите позже...',
                     'Лучше не говорить тебе этого',
                     'Не могу предсказать этого',
                     'Сконцентрируйся и спроси еще раз',
                     "Не расчитывай на это!",
                     'Мой ответ - нет',
                     'Мои источники говорят - нет',
                     'Выглядит не очень хорошо',
                     'Очень сомнительно']
        await ctx.channel.send(f'Вопрос: {question}\nОтвет: {choice(responses)}')

    @commands.command(aliases=['монетка'])
    async def flip(self, ctx, range_x=None, range_y=None):
        money = ['Решка', 'Орел']

        if (range_x or range_y) is not None:
            await ctx.channel.send(f'Выпал номер {randint(int(range_x), int(range_y))}')
        else:
            await ctx.channel.send(f'Выпала сторона: {choice(money)}')

    @commands.command(aliases=['статьи'])
    async def article(self, ctx):
        await ctx.message.delete()
        await ctx.channel.send(f'**Для поиска научных статей на любую тему:**\nhttps://cyberleninka.ru/')

    @commands.command(aliases=['инфо'])
    async def info(self, ctx, member: discord.Member):
        emd = discord.Embed(title=f'Информация о {member.name}', colour=1752220)
        emd.add_field(name='Ник', value=member.nick if member.nick is not None else member.name, inline=True)
        emd.add_field(name='Роль', value=member.top_role)
        emd.add_field(name='Вступил', value=str(member.joined_at)[:16], inline=False)
        emd.add_field(name='Аккаунт создан', value=str(member.created_at)[:16])
        emd.add_field(name='ID', value=member.id, inline=False)
        emd.set_thumbnail(url=member.avatar_url)
        emd.set_footer(text=f'Вызвано: {ctx.message.author}', icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=emd)


def setup(client):
    client.add_cog(OtherCommands(client))
