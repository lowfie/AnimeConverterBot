from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from bot.filter.admin import IsAdmin
from bot.filter.chat_subscriber import IsSubscriber


# register all handlers
async def register_bot_handlers(dispatcher: Dispatcher):
    from bot.handler.start import start
    from bot.handler.help import admin_help
    from bot.handler.stats import stats_of_users
    from bot.handler.cancel_state import cancel_handler
    from bot.handler.bot_blocked import user_blocked_bot
    from bot.handler.shout import cmd_shout, process_text, process_media, FormShout, process_pin_button_to_shout
    from bot.handler.subscriber import add_subscribe, remove_subscribe, get_all_subscriber
    from bot.handler.convert_photo.message_after_photo import (
        text_after_photo,
        process_pin_button,
        process_media_after_photo,
        FormAfterPhoto
    )
    from bot.handler.convert_photo.converter import send_anime_photo
    from bot.handler.chat_join.text_join_chat import (
        text_join_to_chat,
        text_after_join_chat,
        process_media_join_chat,
        process_join_chat_pin_button,
        FormJoinMessage
    )
    from bot.handler.chat_join.approve import approve_member

    # /start - starting bot
    dispatcher.register_message_handler(start, commands="start")

    # /ahelp - all admin commands
    dispatcher.register_message_handler(admin_help, IsAdmin(), commands="ahelp")

    # /stats - get stat of users life
    dispatcher.register_message_handler(stats_of_users, IsAdmin(), commands="stats")

    # handler conversation and send photo
    dispatcher.register_message_handler(send_anime_photo, IsSubscriber(), content_types=["photo"])

    # /cancel - cancel state machine
    dispatcher.register_message_handler(cancel_handler, state="*", commands="cancel")
    dispatcher.register_message_handler(cancel_handler, Text(equals="вернуться к боту", ignore_case=True), state="*")

    # CRUD command for adding button sponsors
    dispatcher.register_message_handler(add_subscribe, IsAdmin(), commands="add_sub")
    dispatcher.register_message_handler(remove_subscribe, IsAdmin(), commands="remove_sub")
    dispatcher.register_message_handler(get_all_subscriber, IsAdmin(), commands="subs")

    # mailing to all users /shout command
    dispatcher.register_message_handler(cmd_shout, IsAdmin(), commands="shout")
    dispatcher.register_message_handler(process_text, content_types=["text"], state=FormShout.text)
    dispatcher.register_message_handler(process_pin_button_to_shout, content_types=["text"], state=FormShout.button)
    dispatcher.register_message_handler(
        process_media,
        content_types=["photo", "video", "animation"],
        state=FormShout.media
    )

    # /text_join_chat , /text_after_chat command
    dispatcher.register_message_handler(text_join_to_chat, IsAdmin(), commands=["text_join_chat", "tjc"])
    dispatcher.register_message_handler(text_after_join_chat, IsAdmin(), commands=["text_after_join", "taj"])
    dispatcher.register_message_handler(
        process_join_chat_pin_button,
        content_types=["text"],
        state=FormJoinMessage.button
    )
    dispatcher.register_message_handler(
        process_media_join_chat,
        content_types=["text", "photo", "video", "animation"],
        state=FormJoinMessage.message
    )

    # /text_after_photo command
    dispatcher.register_message_handler(text_after_photo, IsAdmin(), commands=["text_after_photo", "tap"])
    dispatcher.register_message_handler(
        process_pin_button,
        content_types=["text"],
        state=FormAfterPhoto.button
    )
    dispatcher.register_message_handler(
        process_media_after_photo,
        content_types=["text", "photo", "video", "animation"],
        state=FormAfterPhoto.message
    )
    dispatcher.register_chat_join_request_handler(approve_member)

    # handler user blocked bot
    dispatcher.register_my_chat_member_handler(user_blocked_bot)
