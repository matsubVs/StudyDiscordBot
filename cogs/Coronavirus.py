import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup


class Coronavirus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['тесты'])
    async def total_tests(self, ctx) -> None:

        await ctx.message.delete()
        url_default = 'https://www.worldometers.info/coronavirus/'
        r = requests.get(url_default)
        soup = BeautifulSoup(r.text, 'lxml')

        trs = soup.find_all('tr')
        trs_text = [test.text for test in trs]
        result = []
        for elem in trs_text:
            result.append(elem.split('\n')[-5])

        data = result[1:]
        total = 0
        for test in data:
            if test == '':
                continue
            elif test == '1M pop':
                break
            else:
                test = ''.join([str(num) for num in test.split(',')])
                total += int(test)

        total = list(str(total))
        count_tests = ''
        for num, let in enumerate(total[::-1], start=1):
            if num % 3 == 0:
                count_tests += let + ','
            else:
                count_tests += let

        count_tests = count_tests[::-1]
        print(count_tests)

        await ctx.channel.send(f'**Проведено тестов в мире:** \n`{count_tests}`')

    @commands.command(aliases=['статистика'])
    async def check_stat(self, ctx, country: str = None) -> None:

        await ctx.message.delete()
        url_default = 'https://www.worldometers.info/coronavirus/'
        r = requests.get(url_default)
        soup = BeautifulSoup(r.text, 'lxml')

        result_cases = {'Country':       'N/A',
                        'Total':         'N/A',
                        'New cases':     'N/A',
                        'Deaths':        'N/A',
                        'New Deaths':    'N/A',
                        'Recovered':     'N/A',
                        'Active':        'N/A',
                        'Critical':      'N/A',
                        'Cases/1M pop':  'N/A',
                        'Deaths/1M pop': 'N/A',
                        'Tests':         'N/A',
                        'Tests/1M pop':  'N/A',
                        'Population':    'N/A'
                        }

        if not country:
            covid_counter = soup.find_all('tr')

            covid_counter = [cases for cases in covid_counter if 'World' in str(cases)]
            result = (''.join(covid_counter[0].text)).split('\n')[2:-2]

            i = 0
            file = open('cogs/info_files/if_not_country.txt', mode='w')
            for k, v in result_cases.items():
                file.write(f'**{k}**: `{result[i] if result[i] != "" else v}`\n')
                i += 1

            file.close()

            file = open('cogs/info_files/if_not_country.txt', mode='r')
            await ctx.channel.send(file.read())

        else:
            cases_by_country = soup.find_all('tr')

            cases_chosen_country = [cases for cases in cases_by_country if f'{country}' in str(cases)]
            result = (''.join(cases_chosen_country[0].text)).split('\n')[2:-2]

            i = 0
            file = open('cogs/info_files/total_cases.txt', mode='w')
            for k, v in result_cases.items():
                file.write(f'**{k}**: `{result[i] if result[i] != "" else v}`\n')
                i += 1
            file.close()

            file = open('cogs/info_files/total_cases.txt', mode='r')

            await ctx.channel.send(file.read())
            file.close()


def setup(client):
    client.add_cog(Coronavirus(client))
