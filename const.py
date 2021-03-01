from os import getenv

from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = getenv("DISCORD_BOT_TOKEN")

ID_GUILD = int(getenv("ID_GUILD", "815990947098787850"))
ID_ROLE_BOT = int(getenv("ID_ROLE_BOT", "816006447002550272"))
ID_ROLE_MEMBER = int(getenv("ID_ROLE_MEMBER", "816006513688444950"))
