// voice_video_bot/main.py
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import os
import subprocess
from uuid import uuid4

API_TOKEN = '7958617447:AAEi_efhiSUGwwxOJcUSDlJ3qCCofcKrVsA'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['voice'])
async def handle_voice(message: types.Message):
    text = message.get_args()
    if not text:
        await message.reply("Напиши текст после команды, например: /voice Привет, как дела?")
        return

    filename = f"{uuid4()}.wav"
    os.system(f'echo "{text}" | gtts-cli -l ru -o {filename}')
    await message.reply_voice(voice=InputFile(filename))
    os.remove(filename)

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    video = await message.video.download()
    input_path = video.name
    output_path = f"{uuid4()}.mp4"

    cmd = f"ffmpeg -i {input_path} -vf \"scale=240:240:force_original_aspect_ratio=decrease,pad=240:240:(ow-iw)/2:(oh-ih)/2\" -c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p {output_path}"
    subprocess.run(cmd, shell=True)

    await message.reply_video(video=InputFile(output_path), supports_streaming=True)
    os.remove(input_path)
    os.remove(output_path)

if __name__ == '__main__':
    executor.start_polling(dp)
