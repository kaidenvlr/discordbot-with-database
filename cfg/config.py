import discord
from discord.partial_emoji import PartialEmoji

settings = {
    'token' : 'ENTER YOUR TOKEN HERE',
    'bot' : 'BOT',
    'id' : 'BOT_ID',
    'prefix' : '>',
    
    'channel_welcome_id' : 'WELCOME_CHANNEL_ID',

    'tenor_api_key': 'TENOR_API_KEY'
}

BOT_PREFIX = ">"
your_guild_id = 0
id_of_private_channel_create = 0
private_channels_category = 0
id_role_muted = 0

roles = {
    'KEY': 'VALUE' # 
}

role_message_id = 'MESSAGE ID FOR GIVING ROLES ON ADD EMOTION'
emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 'ROLE', # ID of the role associated with unicode emoji '🔴'.
            discord.PartialEmoji(name='🟠'): 'ROLE', # ID of the role associated with unicode emoji '🟡'.
            discord.PartialEmoji(name='🟢'): 'ROLE', # ID of the role associated with a partial emoji's ID.
            discord.PartialEmoji(name='🔵'): 'ROLE',
            discord.PartialEmoji(name='🟣'): 'ROLE',
            discord.PartialEmoji(name='⚪'): 'ROLE'
        }

ranked_roles = [
    'id_0', 'id_1', 'id_2', 'id_3', 'id_4', 'id_5'
]

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [2, 4, 5, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
green = [0, 37]

year = 2002
month = 4
day = 3
hour = 10
minute = 23
second = 0