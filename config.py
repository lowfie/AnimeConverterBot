from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")

START_FILE_ID = env.str("START_FILE_ID")

JOIN_CHAT_TEXT = env.str("JOIN_CHAT_TEXT")
JOIN_CHAT_FILE_ID = env.str("JOIN_CHAT_ANIMATION")

chats = [
    # format {"title": "", "chat_id": , "invited_link": ""}
]

