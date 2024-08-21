import asyncio
import logging
import pybase64
from PIL import Image
from io import BytesIO

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tg_bot.config import load_config
from tg_bot.models.DBSM import session
import aiogram.types as types

from database import WorkBd, engine

bd_utils = WorkBd(engine)


logger = logging.getLogger(__name__)

def register_all_filters(dp):
    return None

def register_all_handlers(dp):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(get_qr, lambda message: message != '/start')

async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    pvzs = bd_utils.get_pvz()
    for pvz in pvzs:
        button = types.InlineKeyboardButton(str(pvz))
        keyboard.add(button)
    
    await message.answer("choise pvz", reply_markup=keyboard)


async def get_qr(message: types.Message):
    qr_base64 = bd_utils.get_qr(message.text)['qr']
    decoded_data = pybase64.b64decode((qr_base64[22:]))
    img_file = open('myimage.jpeg', 'wb')
    img_file.write(decoded_data)
    img_file.close()

    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

    task = asyncio.create_task(send_photo(bot, message))
    task.add_done_callback(lambda t: t.exception())
    await task
    
    
async def send_photo(bot, message):

    await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile('myimage.jpeg'))

async def main():

    logging.basicConfig(
            level=logging.DEBUG,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
        )
    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    

    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await storage.close()
        await storage.wait_closed()
        await dp.bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
