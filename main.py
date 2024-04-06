import sys
import asyncio
import tools
from discord import Embed, Game, Bot, Option, AutocompleteContext, ApplicationContext
from database.psql import psql
from database.channel_logging import ChannelLogging
from exceptions import *
from typing import List, Dict

# aiopg throwing exception without this
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

cvet = 0xfedbb6
toka: str = ''  # bot token here
ALLOWED_CHANNEL_ID: int = 000000000000000000  # where frame data can be edited
LOGGING_CHANNEL_ID: int = 000000000000000000  # where frame data edits will be logged

postgres = psql.Database()

bot = Bot()
logger: ChannelLogging

cf_character_names: List[str]
tag_character_names: List[str]
cf_move_names: Dict[str, List]
tag_move_names: Dict[str, List]
games_names: List[str] = ['cf', 'tag']

character_selection_embed = Embed(
    description='Select your character below...',
    color=0xfedbb6
)


async def update_character_and_move_names():
    global cf_character_names, tag_character_names, cf_move_names, tag_move_names
    cf_character_names = await get_all_characters_names(database=postgres, game_id=1)
    tag_character_names = await get_all_characters_names(database=postgres, game_id=2)
    cf_move_names = await get_all_move_names(database=postgres, game_id=1)
    tag_move_names = await get_all_move_names(database=postgres, game_id=2)


def get_game_id(option: str) -> int:
    if 'cf' in option.lower():
        return 1
    return 2


def get_game_id_in_ctx(ctx: AutocompleteContext) -> int:
    if 'game_name' in ctx.options.keys():
        return get_game_id(ctx.options['game_name'])
    else:
        return get_game_id(ctx.command.qualified_name)


def autocomplete_parser(items_: list) -> list:
    if len(items_) >= 25:
        result = items_.copy()
        result[24] = 'and more... just start typing!'
        return result
    return items_