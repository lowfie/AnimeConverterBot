import base64
import requests

from settings.config import TOKEN
from bot.base import dp, bot
from bot.utils import anti_flood, get_ai_image


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
    except:
        await bot.send_message(message.from_user.id, "🚨 Произошла ошибка, попробуйте еще раз")
