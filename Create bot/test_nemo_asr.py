import telebot
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
from pydub import AudioSegment
import urllib.request
import nemo.collections.asr as nemo_asr
import datetime
from datetime import timedelta

bot = telebot.TeleBot('6153178579:AAGO3gjJXFTVNcNOIvBmEEOSUcsQq8dLjJQ')
temp_mark_command = 'command_step'
temp_mark_stage = ''
adress = 'ул. Солнечная, 5, г. Новосибирск\n' \
         f"ул. Центральная, 10, г. Москва:\n" \
         f"пр. Ленина, 15, г. Санкт-Петербург\n" \
         f"ул. Лесная, 20, г. Екатеринбург\n" \
         f"ул. Пушкина, 25, г. Казань\n" \
         f"пр. Победы, 30, г. Ростов-на-Дону\n" \
         f"ул. Гагарина, 35, г. Нижний Новгород\n"
contact_info = 'Телефон: +7 (999) 123-45-67\n' \
               f"Email: info@example.com\n" \
               f"Адрес: г. Москва, ул. Пушкина, дом 10, кв. 25\n"
insurance_companies = 'Здоровое будущее\n' \
                      f'Гарант-Мед\n' \
                      f'Промедстрах\n' \
                      f'Страх-Здоровье\n' \
                      f'Медицинское обеспечение\n'
specializations_url = "https://adukar.com/by/news/abiturientu/medicinskie-professii"
doctors_dict = {('аллерг', 'ерголог'): 'Аллерголог', ('инфекц', 'кционист'): 'Инфекционист',
                ('рентген', 'генолог'): 'Рентгенолог',
                ('анестес', 'анестез', 'стезиоло'): 'Анестезиолог',
                ('дермат', 'рматоло'): 'Дерматолог', ('карди', 'диоло'): 'Кардиолог',
                ('офтальм', 'тальмоло'): 'Офтальмолог',
                ('онкол', 'колог'): 'Онколог', ('педи', 'диатор', 'диатор'): 'Педиатр',
                ('психи', 'психе', 'сихиатор'): 'Психиатр', ('стомат', 'томатол'): 'Стоматолог',
                ('урол', 'ролог'): 'Уролог', ('терапевт', 'рапевт'): 'Терапевт',
                ('хирур', 'херур', 'рурк', 'рург'): 'Хирург'}
dates_dict = {('одинад', 'одиннад', 'инадцатого', 'инадцатово', 'инадцатое', '11'): '11',
              ('двена', 'енадцатого', 'венадцатово', 'венадцатое', '12'): '12',
              ('13', 'трина', 'ринадцатого', 'ринадцатово', 'ринадцатое'): '13',
              ('14', 'четырн', 'ырнадцатого', 'ырнадцатово', 'ынадцатое'): '14',
              ('15', 'пятна', 'петна', 'петнадцатое', 'пятнадцатое'): '15',
              ('16', 'шестна', 'снадцатое', 'стнадцатое'): '16', ('17', 'семна', 'семьна'): '17',
              ('18', 'восемна', 'восемьна'): '18',
              ('19', 'девятна', 'вятна'): '19', ('20', 'двацатое', 'ватцатое', 'вадсатое', 'вадцатое'): '20',
              ('21', 'двацать перв', 'двадцать перв', 'дватцать перв', 'дватсать перв'): '21',
              ('22', 'двацать фтор', 'двадцать фтор', 'двацать втор', 'двадцать втор'): '22',
              ('23', 'двацать трет', 'двадцать трет'): '23', ('24', 'двацать четв', 'двадцать четв'): '24',
              ('25', 'двацать пятов', 'двацать пятог', 'двадцать пятов', 'двадцать пятог'): '25',
              ('26', 'двацать шест', 'двадцать шест'): '26',
              ('27', 'двадцать седьм', 'двацать седм', 'двацать седьм', 'двадцать седм'): '27',
              ('28', 'двацать восьм', 'двадцать восьм'): '28',
              ('29', 'двадцать девято', 'двацать девято'): '29',
              ('30', 'трицатое', 'тритцатое', 'ридсатое', 'ридцатое'): '30',
              ('31', 'рицать перв', 'рицат перв', 'ридцать перв', 'ритцать перв', 'ритсать перв'): '31',
              ('01', 'перв', 'ервого', 'ервово'): '01', ('02', 'фтор', 'втор'): '02',
              ('03', 'трет', 'ретьего', 'ретьево'): '03', ('04', 'четв', 'вертого', 'вертово'): '04',
              ('05', 'пятов', 'пятог'): '05', ('06', 'шест', 'стого', 'стово'): '06',
              ('07', 'седьм', 'дьмого', 'дьмово', 'дьмое'): '07', ('08', 'восе', 'сьмого', 'сьмово', 'вось'): '08',
              ('09', 'девято', 'вятовово', 'вятово', 'евять'): '09', ('10', 'десят', 'сятово', 'сятого'): '10'}
month_dict = {('01', 'янв', 'нварь'): '01', ('02', 'февра', 'враля'): '02', ('03', 'март', 'арта'): '03',
              ('04', 'апрел', 'преля'): '04',
              ('05', 'мая', 'май'): '05', ('06', 'июн', 'юня'): '06', ('07', 'июл', 'юля'): '07',
              ('08', 'авгус', 'густа'): '08', ('09', 'сентяб', 'нтября'): '09', ('10', 'октяб', 'ктября'): '10',
              ('11', 'нояб', 'оября'): '11', ('12', 'декаб', 'кабря'): '12'}
time_schedule = ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00',
                 '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00']
times_dict = {('08:30', 'осемь три', 'осемь часов три', 'пол девято'): '08:30',
              ('08:00', 'осемь часов ноль', 'осемь утр', 'осемь ноль', 'осемь час'): '08:00',
              ('09:30', 'девять три', 'девять часов три', 'пол десято'): '09:30',
              ('09:00', 'евять ноль', 'девять часов ноль', 'девять утра', 'евять час'): '09:00',
              ('10:30', 'десять три', 'десять часов три', 'пол один'): '10:30',
              ('10:00', 'есять ноль', 'десять часов ноль', 'десять утра', 'десять час'): '10:00',
              ('11:30', 'одинадцать три', 'одинадцать часов три', 'одиннадцать три', 'одиннадцать часов три',
               'пол двен'): '11:30',
              ('11:00', 'одинадцать ноль', 'одиннадцать ноль', 'одинадцать час', 'одиннадцать час',
               'одинадцать утра', 'одиннадцать утра'): '11:00',
              ('12:30', 'венадцать три', 'венадцать часов три', 'пол перв'): '12:30',
              ('12:00', 'венадцать ноль', 'венадцать час'): '12:00',
              ('13:30', 'тринадцать три', 'час тридцать', 'тринадцать часов три', 'пол втор'): '13:30',
              ('13:00', 'тринадцать ноль', 'час дня', 'в час', 'тринадцать час'): '13:00',
              ('14:30', 'тырнадцать три', 'тырнадцать часов три', 'пол трет', 'два часа тридцать'): '14:30',
              ('14:00', 'тырнадцать ноль', 'два часа дня', 'в два час', 'тырнадцать час'): '14:00',
              ('15:30', 'пятнадцать три', 'пятнадцать часов три', 'пол четв', 'три часа тридцать'): '15:30',
              ('15:00', 'пятнадцать ноль', 'три часа дня', 'в три час', 'пятнадцать час'): '15:00',
              ('16:30', 'cтнадцать три', 'cнадцать три', 'cтнадцать часов три', 'cнадцать часов три', 'пол пят',
               'четыре часа тридцать'): '16:30',
              ('16:00', 'cтнадцать ноль', 'cнадцать ноль', 'четыре часа дня', 'в четыре час', 'cтнадцать час',
               'cнадцать час'): '16:00',
              ('17:30', 'семнадцать три', 'семнадцать часов три', 'пол шест', 'пять часов тридцать'): '17:30',
              ('17:00', 'семнадцать ноль', 'пять часов дня', 'пять часов вечера', 'в пять час',
               'семнадцать час'): '17:00',
              ('18:00', 'восемнадцать ноль', 'шесть часов вечера', 'в шесть час', 'восемнадцать час'): '18:00'}
doctor, patient, date, time, month = '', '', '', '', ''
counter = 0


@bot.message_handler(commands=['start'])
def starting_message(message):
    text = f'Добрый день, {message.from_user.first_name}, выберите одну из команд: \n' \
           f'1) запись ко врачу \n' \
           f"2) Посмотреть расписание \n" \
           f"3) Запрос справочной информации\n"
    bot.send_message(message.chat.id, text)
    global temp_mark_command
    temp_mark_command = 'command_step'


def oga_to_wav(audio_url):
    urllib.request.urlretrieve(audio_url, 'audio.oga')
    src = "audio.oga"
    dst = "audio.wav"
    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")
    voice_url = 'https://api.telegram.org/file/bot{}/{}'.format('6153178579:AAGO3gjJXFTVNcNOIvBmEEOSUcsQq8dLjJQ',
                                                                'audio.wav')
    return voice_url


def transcribe_audio(voice_url: str):
    transcription = ''
    model = nemo_asr.models.EncDecCTCModel.restore_from('../QuartzNet15x5_golos.nemo')
    files = [voice_url]
    transcriptions = model.transcribe(paths2audio_files=files)
    for fname, transcription in zip(files, transcriptions):
        print(f"Audio in {fname} was recognized as: {transcription}")
    return transcription


def get_collection():
    conn_str = "mongodb://localhost:27017"
    client = MongoClient(conn_str)
    return client['chat_bot']


def add_value(c):
    global doctor, date, time, patient
    try:
        c.insert_one({'patient': patient, 'doctor': doctor, 'date': date, 'time': time})
        return True
    except DuplicateKeyError:
        return False


def voice_message_processing(message):
    file = bot.get_file(message.voice.file_id)
    voice_url = 'https://api.telegram.org/file/bot{}/{}'.format('6153178579:AAGO3gjJXFTVNcNOIvBmEEOSUcsQq8dLjJQ',
                                                                file.file_path)
    oga_to_wav(voice_url)
    file = 'audio.wav'
    transcription = transcribe_audio(file)
    return transcription


def get_doctor(t):
    d = ''
    for i in doctors_dict.keys():
        if type(i) == str:
            if i in t.lower():
                d = doctors_dict[i]
                break
        else:
            if any(x in t.lower() for x in list(i)):
                d = doctors_dict[i]
                break
    return d


def get_full_schedule(col, doc):
    global time_schedule
    today = datetime.datetime.now()
    monday = today - timedelta(days=today.weekday())
    dates = [monday + timedelta(days=i) for i in range(5)]
    date_strings = [today.strftime('%d.%m.%Y') for today in dates]
    schedule_dict = dict.fromkeys(date_strings, time_schedule)
    for dt, times in schedule_dict.items():
        query = {'date': dt, 'time': {'$in': times}, 'doctor': doc}
        result = col.find(query)
        for row in result:
            times.remove(row['time'])
    lines = []
    for dt, times in schedule_dict.items():
        times_str = ', '.join(times)
        line = f'{dt}: {times_str}'
        lines.append(line)
    return '\n'.join(lines)


def check_schedule(doc, date_of_check, col):
    global time_schedule
    tmp_times = time_schedule.copy()
    query = {'date': date_of_check, 'doctor': doc}
    result = col.find(query)
    for row in result:
        tmp_times.remove(row['time'])
    return tmp_times


@bot.message_handler(content_types=['text'])
def get_text(message):
    global temp_mark_stage, temp_mark_command, time, patient, doctor, date, counter, month
    transcription = message.text
    if temp_mark_command == 'command_step':
        if any(x in transcription.lower() for x in ['1', 'один', 'перв', 'запис', 'прием']):
            temp_mark_stage = 'assign'
            bot.reply_to(message, 'Чтобы попасть на прием, выберите врача:'
                                  'Аллерголог, Анестезиолог, Дерматолог, Рентгенолог,'
                                  'Кардиолог, Офтальмолог, Онколог, Педиатр, Психиатр,'
                                  'Стоматолог, Уролог, Хирург, Инфекционист, Терапевт')
        elif any(x in transcription.lower() for x in ['2', 'два', 'втор', 'торой', 'распис']):
            temp_mark_stage = 'schedule'
            bot.reply_to(message, 'Выберите врача, чтобы посмотреть свободные даты для записи к нему: '
                                  'Аллерголог, Анестезиолог, Дерматолог, Рентгенолог,'
                                  'Кардиолог, Офтальмолог, Онколог, Педиатр, Психиатр,'
                                  'Стоматолог, Уролог, Хирург, Инфекционист, Терапевт')
        elif any(x in transcription.lower() for x in ['3', 'три', 'трети', 'информ']):
            bot.reply_to(message, 'Секундочку, выводим справочную информацию')
            bot_message = f"Адреса клиник: {adress}\n" \
                          f"Контактные данные медицинских учреждений: {contact_info}\n" \
                          f"Список страховых компаний, с которыми работает наша клиника: {insurance_companies}\n" \
                          f"Информация о различных специализациях врачей: {specializations_url}"
            bot.reply_to(message, bot_message)
        elif counter == 0:
            text = f'Добрый день, {message.from_user.first_name}, выберите одну из команд: \n' \
                   f'1) запись ко врачу \n' \
                   f"2) Посмотреть расписание \n" \
                   f"3) Запрос справочной информации\n"
            bot.send_message(message.chat.id, text)
            temp_mark_command = ''
            counter += 1
        else:
            bot.reply_to(message, 'Попробуйте повторить команду')
            temp_mark_command = ''
        if temp_mark_command == 'command_step':
            temp_mark_command = ''
        else:
            temp_mark_command = 'command_step'
    elif temp_mark_stage == 'assign':
        doctor = get_doctor(transcription)
        if doctor != '':
            bot.reply_to(message, f'Выберите дату для записи к {doctor}у')
            # Доступное даты:
            temp_mark_stage = 'doctor'
        else:
            bot.reply_to(message, 'Не удается определить врача, попробуйте еще раз')
    elif temp_mark_stage == 'doctor':
        for i in dates_dict.keys():
            if any(x in transcription.lower() for x in list(i)):
                date = dates_dict[i]
                break
        for i in month_dict.keys():
            if any(x in transcription.lower() for x in list(i)):
                month = month_dict[i]
                break
        if date != '' and month != '':
            date = f'{date}.{month}.{datetime.date.today().year}'
            bot.reply_to(message, f'Выберите время записи (с 9.00 до 18.00 - прием проходит раз в полчаса)')
            # Доступное время:
            temp_mark_stage = 'date'
        else:
            bot.reply_to(message, 'Не удается определить дату, попробуйте еще раз')
    elif temp_mark_stage == 'date':
        for i in times_dict.keys():
            if any(x in transcription.lower() for x in list(i)):
                time = times_dict[i]
                break
        if time != '':
            bot.reply_to(message, f'Назовите ваше ФИО')
            # Доступное время:
            temp_mark_stage = 'time'
        else:
            bot.reply_to(message, 'Не удается определить время, попробуйте еще раз')
    elif temp_mark_stage == 'time':
        patient = transcription.lower()
        collection = get_collection()['patients']
        check_assign = add_value(collection)
        if not check_assign:
            bot.reply_to(message, f'Ошибка базы данных')
        else:
            bot.reply_to(message, f'Вы записаны к {doctor}у на {time} {date}!')
        # Доступное время:
        temp_mark_stage, doctor, patient, date, time, month = '', '', '', '', '', ''
        temp_mark_command = 'command_step'
    elif temp_mark_stage == 'schedule':
        doctor_schedule = get_doctor(transcription)
        if doctor_schedule != '':
            collection = get_collection()['patients']
            schedule = get_full_schedule(collection, doctor_schedule)
            bot.send_message(message.chat.id, "Ниже указаны свободные даты и время")
            bot.send_message(message.chat.id, text=schedule)
        else:
            bot.reply_to(message, 'Не удается определить врача, попробуйте еще раз')
        temp_mark_command = 'command_step'


@bot.message_handler(content_types=['voice'])
def get_audio(message):
    global temp_mark_stage, temp_mark_command, time, patient, doctor, date, counter, month
    transcription = voice_message_processing(message)
    if temp_mark_command == 'command_step':
        if any(x in transcription.lower() for x in ['один', 'перв', 'запис', 'прием']):
            temp_mark_stage = 'assign'
            bot.reply_to(message, 'Чтобы попасть на прием, выберите врача:'
                                  'Аллерголог, Анестезиолог, Дерматолог, Рентгенолог,'
                                  'Кардиолог, Офтальмолог, Онколог, Педиатр, Психиатр,'
                                  'Стоматолог, Уролог, Хирург, Инфекционист, Терапевт')
        elif any(x in transcription.lower() for x in ['два', 'втор', 'торой', 'распис']):
            temp_mark_stage = 'schedule'
            bot.reply_to(message, 'Выберите врача, чтобы посмотреть свободные даты для записи к нему: '
                                  'Аллерголог, Анестезиолог, Дерматолог, Рентгенолог,'
                                  'Кардиолог, Офтальмолог, Онколог, Педиатр, Психиатр,'
                                  'Стоматолог, Уролог, Хирург, Инфекционист, Терапевт')
        elif any(x in transcription.lower() for x in ['три', 'трети', 'информ']):
            bot.reply_to(message, 'Секундочку, выводим справочную информацию')
            bot_message = f"Адреса клиник: {adress}\n" \
                          f"Контактные данные медицинских учреждений: {contact_info}\n" \
                          f"Список страховых компаний, с которыми работает наша клиника: {insurance_companies}\n" \
                          f"Информация о различных специализациях врачей: {specializations_url}"
            bot.reply_to(message, bot_message)
        elif counter == 0:
            text = f'Добрый день, {message.from_user.first_name}, выберите одну из команд: 1) запись ко врачу \n' \
                   f"2) Посмотреть расписание \n" \
                   f"3) Запрос справочной информации\n"
            bot.send_message(message.chat.id, text)
            temp_mark_command = ''
            counter += 1
        else:
            bot.reply_to(message, 'Попробуйте повторить команду')
            temp_mark_command = ''
        if temp_mark_command == 'command_step':
            temp_mark_command = ''
        else:
            temp_mark_command = 'command_step'
    elif temp_mark_stage == 'assign':
        doctor = get_doctor(transcription)
        if doctor != '':
            bot.reply_to(message, f'Выберите дату для записи к {doctor}у')
            # Доступное даты:
            temp_mark_stage = 'doctor'
        else:
            bot.reply_to(message, 'Не удается определить врача, попробуйте еще раз')
    elif temp_mark_stage == 'doctor':
        for i in dates_dict.keys():
            if any(x in transcription.lower() for x in list(i)):
                date = dates_dict[i]
                break
        for i in month_dict.keys():
            if any(x in transcription.lower() for x in list(i)):
                month = month_dict[i]
                break
        if date != '' and month != '':
            date = f'{date}.{month}.{datetime.date.today().year}'
            bot.reply_to(message, f'Выберите время записи')
            # Доступное время:
            temp_mark_stage = 'date'
        else:
            bot.reply_to(message, 'Не удается определить дату, попробуйте еще раз')
    elif temp_mark_stage == 'date':
        for i in times_dict.keys():
            if any(x in transcription.lower() for x in list(i)):
                time = times_dict[i]
                break
        if time != '':
            bot.reply_to(message, f'Назовите ваше ФИО')
            checker = check_schedule(doctor, date, get_collection()['patients'])
            if time not in checker:
                bot.send_message(message.chat.id, "Данное время уже занято, вот свободное время:")
                bot.send_message(message.chat.id, '\n'.join(checker))
            else:
                temp_mark_stage = 'time'
        else:
            bot.reply_to(message, 'Не удается определить время, попробуйте еще раз')
    elif temp_mark_stage == 'time':
        patient = transcription.lower()
        collection = get_collection()['patients']
        check_assign = add_value(collection)
        if not check_assign:
            bot.reply_to(message, f'Ошибка базы данных')
        else:
            bot.reply_to(message, f'Вы записаны к {doctor}у на {time} {date}!')
        # Доступное время:
        temp_mark_stage, doctor, patient, date, time, month = '', '', '', '', '', ''
        temp_mark_command = 'command_step'
    elif temp_mark_stage == 'schedule':
        doctor_schedule = get_doctor(transcription)
        if doctor_schedule != '':
            collection = get_collection()['patients']
            schedule = get_full_schedule(collection, doctor_schedule)
            bot.send_message(message.chat.id, "Ниже указаны свободные даты и время")
            bot.send_message(message.chat.id, text=schedule)
        else:
            bot.reply_to(message, 'Не удается определить врача, попробуйте еще раз')
        temp_mark_command = 'command_step'


bot.polling(none_stop=True)
