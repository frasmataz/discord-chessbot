import chess
import chess.engine
import os
import json
import re
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
engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')

@client.event
async def on_ready():
    global board
    global state

    print(f'{client.user} has connected to Discord!')
    board = chess.Board()

    state = {}

    state['player_color'] = chess.WHITE

@client.command()
async def reset(ctx):
    global board
    global state

    board = chess.Board()
    await print_board(ctx, board, state)

@client.command()
async def board(ctx):
    global board
    global state
    await print_board(ctx, board, state)

@client.command()
async def move(ctx, move_str=None):
    global board
    global state

    if move_str == None:
        await print_msg(ctx, 'No move provided, usage: !move Bc4')
        return
    
    if state['player_color'] != board.turn:
        await print_msg(ctx, 'it\'s not your turn.')
        return

    if board.is_game_over():
        await print_msg(ctx, 'the game\'s over mate.. move on')
        return
   
    if is_legal_move(board, move_str) == False:
        await print_msg(ctx, 'that\'s not something you can do, use !legalmoves to get all legal moves')
        return
    
    try:
        board.push_san(move_str)
    except e:
        await print_msg(ctx, 'okay i didn\'t understand that, and i don\'t know why i didn\'t understand that')
        return
    
    await print_board(ctx, board, state)

    if board.is_game_over():
        await game_over(ctx, board, state)
    else:
        await ai_move(ctx, board, state)
        if board.is_game_over():
            await game_over(ctx, board, state)

@client.command()
async def legalmoves(ctx):
    global board
    out = 'legal moves: \n'
    for move in board.legal_moves:
        out = out + str(board.san(move)) + ', '

    await print_msg(ctx, out)

@client.command()
async def ping(ctx):
    print('pinged');
    await ctx.send('bing')
    await ctx.send('bong')
    await ctx.send('donkey kong')

@client.command()
async def movehelp(ctx):
    helptxt = """```\
Enter a move with the !move command.  eg:
    !move Be4

Moves are entered in algebraic notation. https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

Each piece type is given a letter:
    King:   K
    Queen:  Q
    Rook:   R
    Bishop: B
    Knight: N
    Pawn:   nothing

Moves are typically given as <piece letter><destination>
    eg: 'Move bishop to e5' is 'Be5'

Since pawns have no letter, advancing a pawn would just look like 'b3'

If multiple pieces of the same type could be moved to the same square, you can disambiguate which piece to move by specifying the rank, file, or both if needed.
    eg: 'Move the rook on the b file to d4' is 'Rbd4'
    or: 'Move the bishop on rank 6 to d4' is 'B6d4'

Captures can be identified with an x.
    eg: 'Bishop captures piece on e2' is 'Bxe2'

To castle king-side: 'O-O'
To castle queen-side: 'O-O-O'

i didn't come up with this don't get mad at me
```"""
    await print_msg(ctx, helptxt)

async def game_over(ctx, board, state):
    await print_msg(ctx, 'GAME OVER');
    if board.result() == '1-0':
        await print_msg(ctx, 'YOU FUCKING WON YOU MAD CUNTS @here');
    elif board.result() == '0-1':
        await print_msg(ctx, 'you lost and you suck');
    elif board.result() == '1/2-1/2':
        await print_msg(ctx, 'it was a draw or a stalemate or something idk yawn');
    await print_msg(ctx, 'Move list if you want to analyse this game for some reason');
    await print_msg(ctx, chess.Board().variation_san(board.move_stack)); 
    await print_msg(ctx, 'Type !reset to play again');

def is_legal_move(board, san):
    try:
        board.parse_san(san)
        return True
    except ValueError:
        return False

    return False

async def ai_move(ctx, board, state):
    if state['player_color'] != board.turn and not board.is_game_over():
        await print_msg(ctx, 'AI is making a move..')
        result = engine.play(board, chess.engine.Limit(time=0.1)).move
        result_str = str(board.san(result))
        await print_msg(ctx, 'AI moved ' + result_str)
        board.push(result)
        await print_board(ctx, board, state)

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

