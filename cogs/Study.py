import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from random import randint
import asyncio
import sqlite3


class Study(commands.Cog):
    def __init__(self, client):
        self.client = client
    #     self.lock = asyncio.Lock()
    #     self.checker.start()
    #     self.checker.restart()

    # async def send_announcements(self):
    #     con = sqlite3.connect('cogs/data/main.db')
    #     cur = con.cursor()
    #     guild = self.client.get_guild(689495182609219700)

    #     lessons = cur.execute('''SELECT * FROM lessons''').fetchall()

    #     if len(lessons) > 0:
    #         lessons_delta = {}
    #         now = datetime.now()

    #         for i, lesson in enumerate(lessons):
    #             db_date, db_time = lesson[1].split()
    #             db_day, db_month = db_date.split('.')
    #             db_hour, db_minute = db_time.split(':')
    #             date = datetime(2020, int(db_month), int(db_day), int(db_hour), int(db_minute))
    #             delta = int((date - now).total_seconds())

    #             if delta > 0:
    #                 lessons_delta[i] = [delta, lesson[0], lesson[2], lesson[3]]
    #             else:
    #                 await self.del_lesson(lesson[0])

    #         lesson_delta_sorted = sorted(lessons_delta.items(), key=lambda x: x[1])

    #         for lesson in lesson_delta_sorted:
    #             if lesson[1][0] <= 900:
    #                 channel = self.client.get_channel(699734278296174602)
    #                 print('lesson', lesson[1][2])
    #                 role = get(guild.roles, name=f'{str(lesson[1][2])} класс')
    #                 ann_embed = discord.Embed(title="Оповещение", description=f"До урока у {role.mention} а "
    #                                                                           f"остаётся 15 минут", color=0xea0006)
    #                 ann_embed.add_field(name="Урок:", value=lesson[1][3], inline=True)
    #                 await channel.send(embed=ann_embed)
    #                 await Study.del_lesson(lesson[0])
    #                 break
    #             else:
    #                 pass

    #     else:
    #         pass

    #     con.close()

    # @tasks.loop(seconds=60.0)
    # async def checker(self):
    #     async with self.lock:
    #         await self.send_announcements()

    # @checker.after_loop
    # async def checker_cancel(self):
    #     if self.checker.is_being_cancelled():
    #         print('\nSOMETHING WRONG IN CHECKER\n')

    # @checker.before_loop
    # async def before_checker(self):
    #     print('waiting...')
    #     await self.client.wait_until_ready()

    @staticmethod
    async def del_lesson(id_l: int):
        if id_l == 0:
            id_l += 1
        con = sqlite3.connect('cogs/data/main.db')
        cur = con.cursor()
        del_lesson = cur.execute(f'''SELECT * FROM lessons WHERE id = {id_l}''').fetchall()
        print(del_lesson)
        cur.execute(f'''DELETE FROM lessons WHERE id = {id_l}''').fetchall()
        con.commit()
        after_del_lesson = cur.execute(f'''SELECT * FROM lessons WHERE id>{id_l}''').fetchall()
        print('after', after_del_lesson)
        if len(after_del_lesson) > 0:
            for idl in after_del_lesson:
                lesson_id = int(idl[0])
                lesson_id_min = lesson_id - 1
                cur.execute('''UPDATE lessons SET id = ? WHERE id = ?''', (lesson_id_min, lesson_id))
                con.commit()
        else:
            pass

        after_del_lesson.clear()
        del_lesson.clear()

    @commands.command(aliases=['кдоске'])
    async def board(self, ctx):
        voice_channel_members = ctx.author.voice.channel.members
        random_member = randint(0, len(voice_channel_members))
        answering = voice_channel_members[random_member]
        print(f'К доске выходит: {answering}')

        await ctx.channel.send(f'К доске выходит {answering.mention} \nВот невезуха!')
        await ctx.message.delete()

    @commands.command(aliases=['добавитьурок'])
    async def add_lesson(self, ctx, date, time, grade, *subjects):
        con = sqlite3.connect('cogs/data/main.db')  # подключаем БД с уроками
        cur = con.cursor()

        d = str(date) + " " + str(time)
        lesson_id = (cur.execute('SELECT MAX(id) FROM lessons').fetchone()[0])
        if not lesson_id:
            lesson_id = 0
        cur.execute(f'''INSERT INTO lessons VALUES ({int(lesson_id) + 1}, "{d}", "{grade.lower()}", 
        "{' '.join(subjects)}")''')
        con.commit()  # вжух вжух запись в бд
        await ctx.author.send('Урок добавлен!')

        await ctx.message.delete()
        con.close()

    @commands.command(aliases=['следурок'])
    async def next_lesson(self, ctx, *grade):
        con = sqlite3.connect('cogs/data/main.db')  # подключаем БД с уроками
        cur = con.cursor()

        if grade:
            grade = grade[0].upper()
            lessons = cur.execute(f'''SELECT * FROM lessons 
                WHERE grade = "{grade}"''').fetchall()
            grade = 'у' + ' ' + grade
        else:
            lessons = cur.execute(f'''SELECT * FROM lessons ''').fetchall()
            grade = ''
        print(lessons)
        if len(lessons) > 0:  # если есть уроки в принципе
            lesson_delta = {}
            now = datetime.now()
            for i, lesson in enumerate(lessons):
                date, time = lesson[1].split()
                d = datetime(2020, int(date.split('.')[1]), int(date.split('.')[0]),
                             int(time.split(':')[0]), int(time.split(':')[1]))
                delta = int((d - now).total_seconds())  # находим разницу между уроками

                if delta > 0:  # проверяем, не прошел ли уже урок
                    lesson_delta[i] = delta
                else:  # в противном случае удаляем урок
                    cur.execute(f"""DELETE FROM lessons
                    WHERE id = {lesson[0]}""")
                    con.commit()
            lesson_delta = sorted(lesson_delta.items(), key=lambda x: x[1])  # сортировка
            nearest = list(lesson_delta)[0][0]  # id ближайшего

            embed = discord.Embed(title=f"Следующий урок {grade}", color=0xd61221)
            txt1 = '' if grade else f' ({lessons[nearest][2]})'
            embed.add_field(name=lessons[nearest][1], value=lessons[nearest][3] + txt1, inline=True)
            await ctx.author.send(embed=embed)

        else:  # если нету уроков
            embed = discord.Embed(title="Уроков нет!",
                                  description=f"Никаких уроков {f' {grade} ' if grade else ''}не запланировано. "
                                              "Можно идти отдыхать, только про домашку не забываем ;)",
                                  color=0x1bcd3f)
            await ctx.author.send(embed=embed)

        await ctx.message.delete()
        con.close()

    @commands.command(aliases=['расписание'])
    async def timetable(self, ctx, *grade):
        con = sqlite3.connect('cogs/data/main.db')  # подключаем БД с уроками
        cur = con.cursor()

        if grade:
            grade = grade[0].upper()
            lessons = cur.execute(f'''SELECT * FROM lessons 
                WHERE grade = "{grade}"''').fetchall()
            grade = 'для ' + grade
        else:
            lessons = cur.execute(f'''SELECT * FROM lessons ''').fetchall()
            grade = ''

        if len(lessons) > 0:  # если есть уроки в принципе
            lesson_delta = {}  # массив, куда записываются id уроков и сколько до них осталось (в секундах)
            now = datetime.now()
            for i, lesson in enumerate(lessons):
                date, time = lesson[1].split()
                d = datetime(2020, int(date.split('.')[1]), int(date.split('.')[0]),
                             int(time.split(':')[0]), int(time.split(':')[1]))
                delta = int((d - now).total_seconds())  # находим разницу между уроками
                if delta > 0:  # проверяем, не прошел ли уже урок
                    lesson_delta[i] = delta
                else:
                    await Study.del_lesson(lesson[0])  # удаляем неакутальные

            lesson_delta = sorted(lesson_delta.items(), key=lambda x: x[1])  # сортировка
            print(lesson_delta)

            embed = discord.Embed(title=f"Расписание {grade}", color=0x1551cc)
            for lesson in lesson_delta:
                cur_les = lessons[lesson[0]]
                cur_grd = f'({cur_les[2]})'  # костыль
                embed.add_field(name=cur_les[1], value=f"[{cur_les[0]}] {cur_les[3]} {'' if grade else cur_grd}",
                                inline=False)
            await ctx.author.send(embed=embed)

        else:  # если нет уроков
            embed = discord.Embed(title="Расписание пусто.",
                                  description=f"Никаких уроков {f' {grade} ' if grade else ''}не запланировано. "
                                              "Можно идти отдыхать, только про домашку не забываем ;)",
                                  color=0x1bcd3f)
            await ctx.author.send(embed=embed)

        await ctx.message.delete()
        con.close()

    @commands.command(aliases=['ученики'])
    async def members(self, ctx):
        class_members = {}
        voice_members = ctx.author.voice.channel.members

        for member in voice_members:
            x = member.nick if member.nick is not None else member.name
            class_members[x] = None

        members_sort = sorted(class_members, key=lambda x: x[0])
        class_members.clear()

        f = open('cogs/info_files/members.txt', mode='w')
        for enum, members in enumerate(members_sort):
            f.write(f"`{enum + 1}. {members}` \n")
        f.close()

        f = open('cogs/info_files/members.txt', mode='r')
        await ctx.channel.send(f.read())
        await ctx.message.delete()

        f.close()

    @commands.command(aliases=['дз'])
    async def homework(self, ctx):
        await ctx.message.pin()
        await ctx.channel.send(f'**Домашнее задание закрепил** {ctx.author.name} @everyone')

    @commands.command(aliases=['список'])
    async def classmates(self, ctx, role):
        await ctx.message.delete()
        mates = get(ctx.guild.roles, name=role + ' класс')
        members = mates.members
        class_mates = {}

        for member in members:
            class_mates[member.display_name] = None
        c_m = sorted(class_mates, key=lambda x: x[0])
        class_mates.clear()

        await ctx.channel.send(f'Список учеников {role} класса:')
        f = open('cogs/info_files/member.txt', mode='w')

        for enum, members in enumerate(c_m):
            f.write(f"`{enum + 1}. {members}` \n")

        f.close()

        f = open('cogs/info_files/member.txt', mode='r')
        await ctx.channel.send(f.read())

        f.close()


def setup(client):
    client.add_cog(Study(client))
