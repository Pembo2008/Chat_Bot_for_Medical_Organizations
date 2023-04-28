import telebot
import os
import json
import requests
import subprocess
import urllib.request
import time
import nemo_asr
# import nemo.collections.asr as nemo_asr

bot = telebot.TeleBot('6153178579:AAGO3gjJXFTVNcNOIvBmEEOSUcsQq8dLjJQ')


@bot.message_handler(commands=['start'])
def starting_message(message):
    text = f'Добрый день, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_text(message):
    if "ривет" in message.text:
        bot.send_message(message.chat.id, 'Приветствую!')
    elif 'запис' in message.text.lower():
        bot.send_message(message.chat.id, 'Выберите врача')
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю')


def oga_to_wav(audio_url):
    file = requests.get(audio_url)
    urllib.request.urlretrieve(audio_url,'audio.oga')
    subprocess.run(["ffmpeg", "-i", 'audio.oga', 'audio.wav'])
    data = open('audio.wav', 'rb')


def get_wav(message):
    # bot.reply_to(message, 'Searching song...')
    data = open('audio.wav', 'rb')
    ret_msg = bot.send_voice(message.chat.id,data)
    file = bot.get_file(ret_msg.voice.file_id)
    voice_url = 'https://api.telegram.org/file/bot{}/{}'.format('6153178579:AAGO3gjJXFTVNcNOIvBmEEOSUcsQq8dLjJQ',
                                                                file.file_path)
    return voice_url


def transcribe_audio(voice_url: str):
    model = nemo_asr.models.EncDecCTCModel.restore_from('./QuartzNet15x5_golos.nemo')
    files = [voice_url]
    transcriptions = model.transcribe(paths2audio_files=files)

    for fname, transcription in zip(files, transcriptions):
      print(f"Audio in {fname} was recognized as: {transcription}")


@bot.message_handler(content_types=['voice'])
def get_audio(message):
    file = bot.get_file(message.voice.file_id)
    voice_url = 'https://api.telegram.org/file/bot{}/{}'.format('6153178579:AAGO3gjJXFTVNcNOIvBmEEOSUcsQq8dLjJQ',
                                                                file.file_path)
    oga_to_wav(voice_url)
    voice_url = get_wav(message)
    transcription = transcribe_audio(voice_url)
    bot.reply_to(message, 'гс распознано!')


bot.polling(none_stop=True)

