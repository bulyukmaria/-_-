import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import speech_recognition as sr

token = '7590644351:AAHxVq0Y5MEMg7mlQREWQWzHgKOHpNqD9KE'

bot = Bot(token)
dp = Dispatcher(bot)
r = sr.Recognizer()

button_audio = KeyboardButton(text="Отправить аудио")
button_materials = KeyboardButton(text="Перейти к полезным материалам")
button_clear_history = KeyboardButton(text="Очистить историю")

keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_audio, button_materials, button_clear_history)

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Здравствуйте! Выберите следующее действие:', reply_markup=keyboard)

@dp.message(F.audio)
async def convert_audio_to_text(message: types.Message):
    splittup = os.path.splitext(message.voice.file_name)
    file_name = f'{splittup[0]}_{message.from_user.full_name}{splittup[1]}'
    try:
        await bot.download(message.voice.file_id, file_name)
        with sr.AudioFile(file_name) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language='ru')
        await message.answer(text)
    except sr.UnknownValueError:
        await message.answer("Извините, я не смог распознать аудио.")
    except sr.RequestError as e:
        await message.answer(f"Ошибка при распознавании: {e}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        if os.path.exists(file_name): #Проверяем существование файла перед удалением
            os.remove(file_name)

@dp.message(F.text == "Перейти к полезным материалам")
async def send_materials(message: types.Message):
    link = "https://github.com/bulyukmaria/-_-"
    await message.answer(f"Перейдите по ссылке: {link}")

@dp.message(F.text == "Очистить историю")
async def clear_history(message: types.Message):
    await message.answer("Диалог очищен!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())