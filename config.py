import discord
import os
from dotenv import load_dotenv

explicit = []

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

variables = {
    'D_TOKEN': os.environ['D_TOKEN'],
    'SERVER_ID': os.environ['SERVER_ID']
}

TOKEN = variables['D_TOKEN']
server_id = variables['SERVER_ID']


def emb():
    emb = discord.Embed(title='Server rules', color=15844367)
    emb.add_field(name='Диванчики', value='Канал для свободного общения.', inline=False)
    emb.add_field(name='N-класс (голосовой канал)', value='Здесь будут проводится уроки, согласно расписанию.',
                  inline=True)
    emb.add_field(name='N-класс (текстовый канал)',
                  value='Здесь учителя будут размещать домашние задания и отвечать на вопросы.', inline=False)
    return emb
