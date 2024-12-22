import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from wikipedia import page, summary, exceptions
import logging

logging.basicConfig(level=logging.INFO)  # для отладки
logger = logging.getLogger(__name__)

TOKEN = '7590644351:AAHxVq0Y5MEMg7mlQREWQWzHgKOHpNqD9KE'

bot = Bot(token=TOKEN)
dp = Dispatcher()


def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Выбор")
    keyboard.add("Очистить историю")
    keyboard.add("Узнать о(б)")
    keyboard.add("Другое")
    return keyboard


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет!", reply_markup=create_keyboard())


@dp.message(lambda message: message.text in ["Выбор", "Очистить историю", "Другое"])
async def handle_service_selection(message: types.Message):
    if message.text == "Выбор":
        await message.answer("Выберите услугу из списка")
    elif message.text == "Очистить историю":
        await message.answer("История очищена.")
    elif message.text == "Другое":
        await message.answer("Что Вы хотите узнать?")


@dp.message(lambda message: message.text == "Узнать о(б)")
async def handle_wikipedia_search(message: types.Message):
    await message.answer("Введите запрос для поиска в Википедии:")


@dp.message(
    lambda message: message.text != "Выбор" and message.text != "Очистить историю" and message.text != "Узнать о(б)" and message.text != "Другое")
async def handle_wikipedia_query(message: types.Message):
    query = message.text
    try:
        result = summary(query, sentences=2)  # 2 предложения из Википедии
        await message.answer(result)
    except exceptions.PageError:
        await message.answer(f"Страница для запроса '{query}' не найдена в Википедии.")
    except exceptions.DisambiguationError as e:
        await message.answer(
            f"Запрос '{query}' неоднозначен. Попробуйте уточнить запрос. Возможные варианты: {', '.join(e.options)}")
    except Exception as e:
        logger.exception(f"Ошибка при поиске в Википедии: {e}")  # Логирование ошибок
        await message.answer(f"Произошла ошибка при поиске: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

