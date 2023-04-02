import base64
import asyncio
import requests

from loguru import logger
from datetime import datetime, timedelta
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from bot.base import dp, bot
from bot.utils import anti_flood, get_ai_image
from bot.utils import send_message_media_types
from settings.config import TOKEN
from database.service import (
    init_chat_message,
    update_chat_message,
    select_chat_message
)


class FormAfterPhoto(StatesGroup):
    message = State()


async def text_after_photo(message: types.Message, state: FSMContext = None):
    await init_chat_message("after_photo")
    await FormAfterPhoto.message.set()
    async with state.proxy() as data:
        data["text_type"] = "after_photo"
    await message.reply("Отправь сообщение уведомления после отправки ботом фото (с медиафайлом)")


async def process_media_after_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "text":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=None
            )
        elif message.content_type == "photo":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.photo[0].file_id
            )
        elif message.content_type == "video":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.video.file_id
            )
        elif message.content_type == "animation":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.animation.file_id
            )
    await message.reply("Данные были обновлены")
    await state.finish()


@dp.throttled(anti_flood, rate=0.5)
async def send_anime_photo(message):
    await bot.send_message(message.from_user.id, "🤖Нейросеть конвертирует фото")

    # Получаем ID фоторгафии
    fileID = message.photo[-1].file_id
    file = await bot.get_file(fileID)

    # Скачиваем фотографию
    r = requests.get(
        "https://api.telegram.org/file/bot" + TOKEN + "/" + file.file_path,
        timeout=None,
        stream=True,
    )

    # Преобразовываем картинку в base64
    base64_image_string = base64.b64encode(r.content).decode("utf-8")

    # Получаем ссылку на обработанное изображение
    me = await bot.get_me()
    tag = me.username
    try:
        ai_image = get_ai_image(base64_image_string)["media_info_list"][0]["media_data"]
        await bot.send_photo(message.from_user.id, ai_image, caption=f"@{tag}")

        after_photo_content_type, after_photo_text, after_photo_file_id = await select_chat_message("after_photo")
        send_date = datetime.now() + timedelta(seconds=10)
        while datetime.now() <= send_date:
            await asyncio.sleep(1)
            if datetime.now() >= send_date:
                await send_message_media_types(
                    bot=bot,
                    content_type=after_photo_content_type,
                    chat_id=message.from_user.id,
                    text=after_photo_text,
                    file_id=after_photo_file_id
                )
                break
    except Exception as _ex:
        logger.warning("Ошибка нейросети", _ex)
        await bot.send_message(message.from_user.id, "🚨 Произошла ошибка, попробуйте еще раз")
