import chess
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
    global board
    global state

    print(f'{client.user} has connected to Discord!')
    board = chess.Board()

    state = {}

    state['player_color'] = chess.WHITE

@client.command()
async def resetboard(ctx):
    global board
    global state

    board = chess.Board()
    await print_board(ctx, board, state)

@client.command()
async def move(ctx, move):
    global board
    global state

    try:
        board.push_san(move)
    except ValueError:
        await print_msg(ctx, 'you can\'t do that you tit')
        return

    await print_board(ctx, board, state)
    

@client.command()
async def getlegalmoves(ctx):
    global board
    out = 'Your current legal moves are: \n'
    for move in board.legal_moves:
        out = out + str(board.san(move)) + ', '

    await print_msg(ctx, out)

@client.command()
async def ping(ctx):
    print('pinged');
    await ctx.send('bing')
    await ctx.send('bong')
    await ctx.send('donkey kong')

async def print_status(ctx, board, state):
    out = ''
    
    out = out + 'Turn {}, '.format(board.fullmove_number)

    if board.is_game_over():
        if board.is_checkmate():
            out = out + 'Checkmate bitch\n'
        elif board.is_stalemate():
            out = out + 'Stalemate.\n'
    else:
        if board.turn == chess.WHITE:
            out = out + 'white to play\n'
        elif board.turn == chess.BLACK:
            out = out + 'black to play\n'

        if board.is_check():
            out = out + 'Check!\n'

        if state['player_color'] == board.turn:
            out = out + 'It is your move\n'

    await print_msg(ctx, out)
    
async def print_msg(ctx, msg):
    print(msg)
    await ctx.send(msg)

async def print_board(ctx, board, state):
    emojis = get_emojis(ctx)

    out = ''
    for rank in range(7, -1, -1):
        out = out + emojis[str(rank+1)]
        for file_ in range(0, 8):
            square_color = 'light_square' if (rank % 2 == 0) != (file_ % 2 == 0) else 'dark_square'
            piece = board.piece_at(chess.square(file_, rank))
            
            emoji = emojis[square_color]['empty']

            if piece != None:
                emoji = emojis[square_color][piece.symbol()]

            out = out + emoji
        out = out + '\n'
    out = out + emojis['axis']
    
    for i in range (1, 9):
        out = out + emojis[n2l(i)]

    await ctx.send(out)
    await print_status(ctx, board, state)
            

def get_emoji_code(emoji_name, ctx):
    emoji = get(ctx.message.guild.emojis, name=emoji_name)
    return '<:{}:{}>'.format(emoji.name, emoji.id)

def get_emojis(ctx):
    return {
        'light_square': {
            'empty': ':white_large_square:',
            'P': get_emoji_code('wpws', ctx),
            'N': get_emoji_code('wnws', ctx),
            'B': get_emoji_code('wbws', ctx),
            'R': get_emoji_code('wrws', ctx),
            'Q': get_emoji_code('wqws', ctx),
            'K': get_emoji_code('wkws', ctx),
            'p': get_emoji_code('bpws', ctx),
            'n': get_emoji_code('bnws', ctx),
            'b': get_emoji_code('bbws', ctx),
            'r': get_emoji_code('brws', ctx),
            'q': get_emoji_code('bqws', ctx),
            'k': get_emoji_code('bkws', ctx)
        },
        'dark_square': {
            'empty': ':black_large_square:',
            'P': get_emoji_code('wpbs', ctx),
            'N': get_emoji_code('wnbs', ctx),
            'B': get_emoji_code('wbbs', ctx),
            'R': get_emoji_code('wrbs', ctx),
            'Q': get_emoji_code('wqbs', ctx),
            'K': get_emoji_code('wkbs', ctx),
            'p': get_emoji_code('bpbs', ctx),
            'n': get_emoji_code('bnbs', ctx),
            'b': get_emoji_code('bbbs', ctx),
            'r': get_emoji_code('brbs', ctx),
            'q': get_emoji_code('bqbs', ctx),
            'k': get_emoji_code('bkbs', ctx)
        },
        'a': ':regional_indicator_a:',
        'b': ':regional_indicator_b:',
        'c': ':regional_indicator_c:',
        'd': ':regional_indicator_d:',
        'e': ':regional_indicator_e:',
        'f': ':regional_indicator_f:',
        'g': ':regional_indicator_g:',
        'h': ':regional_indicator_h:',
        '1': ':one:',
        '2': ':two:',
        '3': ':three:',
        '4': ':four:',
        '5': ':five:',
        '6': ':six:',
        '7': ':seven:',
        '8': ':eight:',
        'axis': ':heart_decoration:'
    }

def n2l(n):
    return {
        1: 'a',
        2: 'b',
        3: 'c',
        4: 'd',
        5: 'e',
        6: 'f',
        7: 'g',
        8: 'h'
    }[n]

#If there is an error, it will answer with an error
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'i shitted myself: {error}')

client.run(token)

