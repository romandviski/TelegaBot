###############################################
#            СупИр телеграм бот               # 
#                                             #  
#  Дата создания: 26.01.2022                  #
#  Автор: Ефремов Михаил                      #
###############################################


import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.common import register_handlers_common
from app.handlers.status import register_handlers_status
from app.handlers.positive import register_handlers_positive
from app.handlers.negative import register_handlers_negative
from app.handlers.comment import register_handlers_comment

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    # Команды для меню
    commands = [
        BotCommand(command="/status", description="Статус"),
        BotCommand(command="/positive", description="Одобрить"),
        BotCommand(command="/negative", description="Обозлить"),
        BotCommand(command="/comment", description="Комментировать"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp, config.tg_bot.admin_id)
    register_handlers_status(dp)
    register_handlers_positive(dp)
    register_handlers_negative(dp)
    register_handlers_comment(dp)
    

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
