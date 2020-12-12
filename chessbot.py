import os
import json
from pprint import pprint
import discord
from discord.utils import get
from discord.ext import commands

token = ''
guild_id = ''
emoji_names = ''

with open('props.json') as json_file:
    data = json.load(json_file)
    token = data['discord_token']
    guild_id = data['guild_id']
    emoji_names = data['emoji_names']

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def ping(ctx):
    print('pinged');
    await ctx.send('pong')

@client.command()
async def testboard(ctx):
    await ctx.send(':brws::bnbs::bbws::bqbs::bkws::bbbs::bnws::brbs:\n:bpbs::bpws::bpbs::bpws::bpbs::bpws::bpbs::bpws:\n:white_large_square::black_large_square::white_large_square::black_large_square::white_large_square::black_large_square::white_large_square::black_large_square:\n:black_large_square::white_large_square::black_large_square::white_large_square::black_large_square::white_large_square::black_large_square::white_large_square:\n:white_large_square::black_large_square::white_large_square::black_large_square::white_large_square::black_large_square::white_large_square::black_large_square:\n:black_large_square::white_large_square::black_large_square::white_large_square::black_large_square::white_large_square::black_large_square::white_large_square:\n:wpws::wpbs::wpws::wpbs::wpws::wpbs::wpws::wpbs:\n:wrbs::wnws::wbbs::wqws::wkbs::wbws::wnbs::wrws:')

@client.command()
async def testemoj(ctx):
    emojis = get_emojis(ctx)
    emoji = emojis['dark_square']['white']['knight']
    msg = 'shleeeem ' + emoji
    await ctx.send(msg)

def get_emoji_code(emoji_name, ctx):
    emoji = get(ctx.message.guild.emojis, name=emoji_name)
    return '<:{}:{}>'.format(emoji.name, emoji.id)

def get_emojis(ctx):
    return {
        'light_square': {
            'empty': ':white_large_square:',
            'white': {
                'pawn': get_emoji_code('wpws', ctx),
                'knight': get_emoji_code('wnws', ctx),
                'bishop': get_emoji_code('wbws', ctx),
                'rook': get_emoji_code('wrws', ctx),
                'queen': get_emoji_code('wqws', ctx),
                'king': get_emoji_code('wkws', ctx)
            },
            'black': {
                'pawn': get_emoji_code('bpws', ctx),
                'knight': get_emoji_code('bnws', ctx),
                'bishop': get_emoji_code('bbws', ctx),
                'rook': get_emoji_code('brws', ctx),
                'queen': get_emoji_code('bqws', ctx),
                'king': get_emoji_code('bkws', ctx)
            }
        },
        'dark_square': {
            'empty': ':black_large_square:',
            'white': {
                'pawn': get_emoji_code('wpbs', ctx),
                'knight': get_emoji_code('wnbs', ctx),
                'bishop': get_emoji_code('wbbs', ctx),
                'rook': get_emoji_code('wrbs', ctx),
                'queen': get_emoji_code('wqbs', ctx),
                'king': get_emoji_code('wkbs', ctx)
            },
            'black': {
                'pawn': get_emoji_code('bpbs', ctx),
                'knight': get_emoji_code('bnbs', ctx),
                'bishop': get_emoji_code('bbbs', ctx),
                'rook': get_emoji_code('brbs', ctx),
                'queen': get_emoji_code('bqbs', ctx),
                'king': get_emoji_code('bkbs', ctx)
            }
        }
    }

#If there is an error, it will answer with an error
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'i shitted myself: {error}')

client.run(token)

