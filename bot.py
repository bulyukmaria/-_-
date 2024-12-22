from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import speech_recognition as sr
import asyncio
import os

token = '7590644351:AAHxVq0Y5MEMg7mlQREWQWzHgKOHpNqD9KE'

bot = Bot(token)
dp = Dispatcher()
r = sr.Recognizer()

#cоздание клавиатуры с кнопками (ошибка)
button_audio = KeyboardButton(text="Отправить аудио")
button_materials = KeyboardButton(text="Перейти к полезным материалам")
button_clear_history = KeyboardButton(text="Очистить историю")

#используем метод add для добавления кнопок в клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_audio, button_materials, button_clear_history)

#приветствие
@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Здравствуйте! Выберите следующее действие:')

@dp.message(F.text =="Отправить аудио")  #бот работает только с аудио при F.audio
async def convert_audio_to_text(message: types.Message):
    splittup = os.path.splitext(message.audio.file_name)  #сохранение имени и расширения полученного файла
    file_name = f'{splittup[0]}_{message.from_user.full_name}{splittup[1]}'  #формат: имя_пользователя.расширение
    await bot.download(message.audio.file_id, file_name)  #скачивание файла

    #преобразование аудио в текст
    with sr.AudioFile(file_name) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ru')
    await message.answer(text)

    os.remove(file_name)

@dp.message(F.text == "Перейти к полезным материалам")
async def send_materials(message: types.Message):
    link = "https://github.com/bulyukmaria/-_-"
    await message.answer(f"Перейдите по ссылке: {link}")

@dp.message(F.text == "Очистить историю")
async def clear_history(message: types.Message):
    await message.answer("Диалог очищен!")


#удаление предыдущих действий
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
