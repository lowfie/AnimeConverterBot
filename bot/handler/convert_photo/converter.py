import base64
import asyncio
import requests

from loguru import logger
from datetime import datetime, timedelta
from aiogram import types

from bot.base import dp, bot
from bot.utils import anti_flood, get_ai_image, send_message_media_types
from settings.config import TOKEN, FORWARD_CHAT_ID
from database.service import select_chat_message


@dp.throttled(anti_flood, rate=0.5)
async def send_anime_photo(message: types.Message):
    await bot.send_message(message.from_user.id, "🤖Нейросеть конвертирует фото")

    if FORWARD_CHAT_ID:
        text = f"<b>ID пользователя:</b> <code>{message.from_user.id}</code>\n" \
               f"<b>Тег:</b> @{message.from_user.username}"
        try:
            await bot.send_photo(
                chat_id=FORWARD_CHAT_ID,
                photo=message.photo[0].file_id,
                caption=text,
                parse_mode="HTML"
            )
        except Exception as _ex:
            logger.warning("Ошибка пересылки в канал", _ex)

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

        content_type, text, file_id, button_text, button_url = await select_chat_message("after_photo")

        send_date = datetime.now() + timedelta(seconds=10)
        while datetime.now() <= send_date:
            await asyncio.sleep(1)
            if datetime.now() >= send_date:
                await send_message_media_types(
                    bot=bot,
                    content_type=content_type,
                    chat_id=message.from_user.id,
                    text=text,
                    file_id=file_id,
                    button_text=button_text,
                    button_url=button_url
                )
                break
    except Exception as _ex:
        logger.warning("Ошибка нейросети", _ex)
        await bot.send_message(message.from_user.id, "🚨 Произошла ошибка, попробуйте еще раз")
