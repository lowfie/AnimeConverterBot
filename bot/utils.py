import json
import requests
from loguru import logger

from aiogram import types, Bot
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation

from database.service import set_life_user


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("Не флуди, я тебя с первого раза понял!")


async def send_message_media_types(bot: Bot, content_type: str, chat_id, text: str, file_id: str = None):
    try:
        if content_type == "text":
            await bot.send_message(
                chat_id,
                text=text,
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif content_type == "photo":
            await bot.send_photo(
                chat_id,
                photo=file_id,
                caption=text,
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif content_type == "video":
            await bot.send_video(
                chat_id,
                video=file_id,
                caption=text,
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif content_type == "animation":
            await bot.send_animation(
                chat_id,
                animation=file_id,
                caption=text,
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
    except (BotBlocked, CantInitiateConversation):
        await set_life_user(life_status=False, tg_id=chat_id)
        logger.warning(f"Пользователь с ID {chat_id} заблокировал бота")


def get_ai_image(base64_image_string):
    headers = {
        "Connection": "keep-alive",
        "phone_gid": "2862114434",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G955N Build/NRD90M.G955NKSU1AQDC; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 com.meitu.myxj/11270(android7.1.2)/lang:ru/isDeviceSupport64Bit:false MTWebView/4.8.5",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://titan-h5.meitu.com",
        "X-Requested-With": "com.meitu.meiyancamera",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://titan-h5.meitu.com/",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    params = {
        "api_key": "237d6363213c4751ba1775aba648517d",
        "api_secret": "b7b1c5865a83461ea5865da3ecc7c03d",
    }

    json_data = {
        "parameter": {
            "rsp_media_type": "url",
            "strength": 0.45,
            "guidance_scale": 7.5,
            "prng_seed": "-1",
            "num_inference_steps": "50",
            "extra_prompt": "",
            "extra_negative_prompt": "",
            "random_generation": "False",
            "type": "1",
            "type_generation": "True",
            "sensitive_words": "white_kimono",
        },
        "extra": {},
        "media_info_list": [
            {
                "media_data": base64_image_string,
                "media_profiles": {
                    "media_data_type": "jpg",
                },
            },
        ],
    }

    response = requests.post(
        "https://openapi.mtlab.meitu.com/v1/stable_diffusion_anime",
        params=params,
        headers=headers,
        json=json_data,
    )
    return json.loads(response.content)
