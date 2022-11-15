from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, MediaGroup
from asyncio import sleep
import logging

from random import randint, choices
import re
import string
import os
from dotenv import load_dotenv, find_dotenv

from courses import Courses
from database import Database
from markups import mainMenu, playNumb, registrationNow, likeVote, trainList, coursesList, courseTheWay, courseOffline, \
    courseOnline, replyMenu, passwordGenerate

logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv())
bot = Bot(os.getenv('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database('database.db')
db2 = Courses('courses.db')


class ProfileStateGroup(StatesGroup):
    name = State()
    login = State()
    password = State()
    email = State()


# создаем нужные переменные
regexLogin = '/^[A-Za-z0-9_]{3,16})$/'
regexEmail = '/[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}/igm'
arr_teachers = ['static/teachers/teacher1.png', 'static/teachers/teacher2.png', 'static/teachers/teacher4.png',
                'static/teachers/teacher5.png', 'static/teachers/teacher6.png', 'static/teachers/teacher7.png',
                'static/teachers/teacher8.png', 'static/teachers/teacher9.png',
                'static/teachers/teacher10.png', 'static/teachers/teacher11.png']
arr_learning = ['static/opportunities/benefit1.png', 'static/opportunities/benefit2.png',
                'static/opportunities/benefit3.png', 'static/opportunities/benefit4.png',
                'static/opportunities/benefit5.png']

HELP_COMMANDS = """
<b>/start</b> - <em>Начало работы</em>
<b>/help</b> - <em>Помощь</em>
<b>/description</b> - <em>Описание бота</em>
<b>/bonus</b> - <em>Получить бонус</em>
<b>/registration</b> - <em>Регистрация</em>"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('Я запущен и работаю отлично!')
    await db.create_table()
    photo_bytes = InputFile(path_or_bytesio='static/course.jpg')

    await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes,
                         caption=f'Привет, <b>{message.from_user.username}! Добро пожаловать в чат-бот IT "OVERONE"!</b>',
                         parse_mode='HTML')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Введи команду <b>/help</b>, чтобы узнать список возможных действий.\n'
                                'Или воспользуйся <u>меню</u> ниже',
                           parse_mode='HTML', reply_markup=mainMenu)
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_me(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=HELP_COMMANDS,
                           parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['description'])
async def description(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<u>Чат-бот IT "OVERONE" - является упрощенной копией сайта.</u>\n'
                                'Здесь ты можешь найти всю полезную для себя информацию по обучающим курсам, '
                                'проводимым в рамках нашей компании.\n'
                                'Также бот поделится с тобой информацией о преподавательском составе. '
                                'И покажет лучшего преподавателя по мнению учащихся.\n'
                                'Ну и напоследок ты можешь зарегистрироваться, чтобы получить приятные бонусы '
                                'от IT "OVERONE" и быть в курсе последних новостей компании.\n'
                                'Введи команду <b>/help</b>, чтобы узнать список возможных действий.',
                           parse_mode='HTML')
    await message.delete()


# организация рассылки сообщений
@dp.message_handler(commands=['sendall'])
async def send_all(message: types.Message):
    # if message.chat.type == 'private':
    if message.from_user.id == 5374818134:  # админский id
        text = message.text[9:]
        users = db.get_users()
        for user_elem in users:
            try:
                await bot.send_message(user_elem[0], text)
                if int(user_elem[7]) != 1:
                    db.set_active(user_elem[0], 1)
            except:
                db.set_active(user_elem[0], 0)
        await bot.send_message(chat_id=message.from_user.id, text='Успешная рассылка!')


# Получение бонусов
@dp.message_handler(commands=['bonus'])
async def on_message(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Привет, <b>{message.from_user.username}</b>! Добро пожаловать в чат-бот IT "OVERONE"!'
                                f'\nДавай сыграем в <b>игру</b>. Я загадаю случайное число от 1 до 6. А ты подкинешь '
                                f'кубик.\nЕсли ты выиграешь, IT "OVERONE" подарит тебе <u>скидку в 50% на обучение</u>!',
                           parse_mode='HTML', reply_markup=playNumb)


# регистрация пользователя
@dp.message_handler(commands=['registration'], state=None)
async def check_registration(message: types.Message):
    # if message.chat.type == 'private':
    if not db.user_exists(message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<b>Добро пожаловать на регистрацию</b>!\n'
                                    f' Укажи свое имя',
                               parse_mode='HTML')
        await ProfileStateGroup.name.set()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<b>Вы уже зарегистрированы</b>! Вы можете просмотреть свой профиль и выйти в '
                                    f'основное меню.',
                               parse_mode='HTML', reply_markup=replyMenu)
    await message.delete()


# первый ответ и запись в словарь
@dp.message_handler(state=ProfileStateGroup.name)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await ProfileStateGroup.next()
        await message.reply(text='Придумай и укажи логин')


# второй ответ и запись в словарь
@dp.message_handler(state=ProfileStateGroup.login)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 16 < len(message.text) < 3:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Логин должен быть больше 3, но меньше 16 символов')
        elif re.match(r'regexLogin', str(message.text)):
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Логин содержит запрещенные символы, повтори попытку')
        data['login'] = message.text
        await ProfileStateGroup.next()
        await message.reply(text='Сгенерируй пароль', reply_markup=passwordGenerate)


# третий ответ и запись в словарь
@dp.message_handler(state=ProfileStateGroup.password)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        passwordData = ''.join(choices(string.ascii_lowercase + string.ascii_uppercase, k=15))
        data['password'] = passwordData
        await ProfileStateGroup.next()
        await message.reply(text='Укажи свой e-mail')


# четвертый ответ и запись в словарь
@dp.message_handler(state=ProfileStateGroup.email)
async def add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if re.match(r'regexEmail', str(message.text)):
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Твой e-mail недействительный, введи правильный e-mail')
        data['email'] = message.text

    data = await state.get_data()
    name = data.get('name')
    login = data.get('login')
    password = data.get('password')
    email = data.get('email')

    await message.reply(text=f'<b>Регистрация прошла успешно</b>!\n'
                             f'Твое имя {name}\n'
                             f'Твое логин {login}\n'
                             f'Твой пароль {password}\n'
                             f'Твой e-mail {email}',
                        parse_mode='HTML', reply_markup=mainMenu)

    await db.add_profile(state=state, user_id=message.from_user.id)
    if db.get_sign_up(message.from_user.id) == 'setlogin':
        db.set_sign_up(message.from_user.id, 'done')

    await state.finish()


@dp.message_handler()
async def detect_message_text(message: types.Message):
    # Информация о партнерах
    match message.text:
        # подписка(не реализована полноценно)
        case 'Подписка':

            await message.answer(text='Тарифы на подписку')
            await message.delete()
        # получение профиля
        case 'Профиль':

            await bot.send_message(chat_id=message.from_user.id, text=db.get_user(message.from_user.id),
                                   reply_markup=mainMenu)
            await message.delete()
        case 'Наши партнеры':

            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Представители IT-компаний</b> знакомы с качеством нашего обучения. И '
                                        f'поэтому с удовольствием берут наших студентов на стажировку с дальнейшим '
                                        f'трудоустройство.\n'
                                        '<em>Присоединяйся к нашей команде!!!</em>',
                                   parse_mode='HTML')
            photo_bytes = InputFile(path_or_bytesio='static/partners.png')
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
            await message.delete()

        # Показ рандомных преподавателей по запросу
        case 'Наши преподаватели':

            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Наши преподаватели</b> - лучшие конкурентные специалисты в IT-сфере,'
                                        'имеющие большой практический опыт коммерческой разработки.',
                                   parse_mode='HTML')
            await message.delete()

            album = MediaGroup()
            while True:
                for photo_teacher in arr_teachers:
                    photo_bytes = InputFile(path_or_bytesio=photo_teacher)
                    album.attach_photo(photo=photo_bytes)
                await message.answer_media_group(media=album)
                break

            await sleep(1)
            photo_bytes = InputFile(path_or_bytesio='static/teachers/teacher3.png')

            await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes,
                                 caption=f'<b><i>Лучший преподаватель по мнению учащихся</i></b>.\n'
                                         'Ты можешь оценить работу преподавательского состава в общем,'
                                         'если ты уже знаком с кем-то из преподавателей))).\n',
                                 parse_mode='HTML', reply_markup=likeVote)

        # как построено обучение
        case 'Об обучении':

            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>А теперь несколько слайдов о том, как построено наше обучение</b>',
                                   parse_mode='HTML')
            await message.delete()

            for photo_slide in arr_learning:
                photo_bytes = InputFile(path_or_bytesio=photo_slide)
                await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
                await sleep(1)

        # тренинги
        case 'Наши тренинги':
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<u>Специально для наших студентов. КМР от IT "OVERONE".</u>\n'
                                        '<b>КМР - это курс молодого разработчика.</b> '
                                        'Мы собрали отзывы студентов и сделали этот набор продуктов.\n'
                                        'Ты в 2 раза быстрее вольешься в сферу IT и обучение пойдет намного проще.',
                                   parse_mode='HTML', reply_markup=trainList)
            await message.delete()

        # обучающие курсы общая
        case 'Обучающие курсы':
            photo_bytes = InputFile(path_or_bytesio='static/course.jpg')

            await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes,
                                 caption=f'<b>IT "OVERONE" заботится о студентах! Присоединяйся к нашей команде! '
                                         'Вместе мы команда!</b>', parse_mode='HTML')
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'Наша компания предоставляет возможность обучения в зависимости '
                                        'от твоей занятости:\n'
                                        '1. <b>индивидуальное обучение (The way)</b> в удобное время в удобном темпе.\n'
                                        '2. <b>offline-обучение</b> с преподавателем в обустроенных аудиториях.\n'
                                        '3. <b>online-обучение</b> не выходя из дома.',
                                   parse_mode='HTML', reply_markup=coursesList)
            await message.delete()

        # TheWay-обучение
        case 'TheWay-обучение':
            photo_bytes = InputFile(path_or_bytesio='static/courses/theway.png')

            await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>THE WAY - индивидуальное обучение</b> с опытным преподавателем, '
                                        'адаптированное под ваши цели.',
                                   parse_mode='HTML', reply_markup=courseTheWay)
            await message.delete()

        # Offline-обучение
        case 'Offline-обучение':
            photo_bytes = InputFile(path_or_bytesio='static/courses/offline.png')

            await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b><u>OFFLINE-обучение.</u></b>\n'
                                        'Максимум практики. Теоретические основы.\n'
                                        'Домашние задания. Небольшие группы. \n'
                                        'Сертификат. Сопровождение специалистов, полное оформление необходимой рабочей '
                                        'документации (резюме, портфолио, LinkedIn).\n'
                                        'Поддержка 24/7!',
                                   parse_mode='HTML', reply_markup=courseOffline)
            await message.delete()

        # Online-обучение
        case 'Online-обучение':
            photo_bytes = InputFile(path_or_bytesio='static/courses/online.png')

            await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b><u>ONLINE-обучение.</u></b>\n'
                                        'Максимум практики. Теоретические основы.\n'
                                        'Домашние задания. Небольшие группы. \n'
                                        'Сертификат. Сопровождение специалистов, полное оформление необходимой рабочей '
                                        'документации (резюме, портфолио, LinkedIn).\n'
                                        'Поддержка 24/7!',
                                   parse_mode='HTML', reply_markup=courseOnline)
            await message.delete()


@dp.callback_query_handler()
async def detect_callback_data(call: types.CallbackQuery):
    global bot_data
    match call.data:
        case 'RegistrationList':
            await call.message.answer(text=f'Нажми <b>/registration</b> и ответь пожалуйста на несколько вопросов',
                                      parse_mode='HTML')
        case 'NonRegistration':
            await call.message.answer(text='Хорошо, давай продолжим без регистрации... Однако ты упускаешь возможность '
                                           'получить ценные подарки и бонусы от нашей компании',
                                      reply_markup=mainMenu)
        # получение бонусов
        case 'RandomNumber':
            bot_data = randint(1, 6)
            await call.message.answer(text="Мое число: {0}".format(bot_data))
        case 'DeviceNumber':
            user_data = await bot.send_dice(call.from_user.id)
            user_data = user_data['dice']['value']
            await sleep(6)
            await call.message.answer(text="Твое число: {0}".format(user_data))

            if bot_data > user_data:
                photo_bytes = InputFile(path_or_bytesio='static/free.png')

                await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
                await bot.send_message(chat_id=call.from_user.id,
                                       text=f'<b>Ты проиграл!</b> Но не унывай, мы дарим тебе '
                                            'возможность посетить наше <u>БЕСПЛАТНОЕ занятие!</u>\n'
                                            'Для этого пройди небольшую <b><i>регистрацию</i></b>. Спасибо)))',
                                       parse_mode='HTML', reply_markup=registrationNow)
            elif bot_data < user_data:
                photo_bytes = InputFile(path_or_bytesio='static/free.png')

                await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
                await bot.send_message(chat_id=call.from_user.id,
                                       text=f'👏 <b>Ты выиграл!</b> Наш менеджер свяжется с тобой для '
                                            'дальнейшего сотрудничества!\n'
                                            'Для этого пройди небольшую <b><i>регистрацию</i></b>. Спасибо)))',
                                       parse_mode='HTML', reply_markup=registrationNow)
            else:
                photo_bytes = InputFile(path_or_bytesio='static/free.png')

                await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
                await bot.send_message(chat_id=call.from_user.id,
                                       text=f'👏 <b>Ничья!</b> Я уступаю тебе победу! Ты выиграл '
                                            'скидку! Менеджер свяжется с тобой в ближайшее время.\n'
                                            'Для этого пройди небольшую <b><i>регистрацию</i></b>. Спасибо)))',
                                       parse_mode='HTML', reply_markup=registrationNow)

        # Оценка преподавателей
        case 'like':
            await call.answer(text='Спасибо за оценку!!! Нам важен каждый отзыв!!!')
        case 'dislike':
            await call.answer(text='Спасибо за оценку!!! Мы тебе услышали. Нам важен каждый отзыв!!!')

        # получение информации по проводимым тренингам
        case 'ITStart':
            photo_bytes = InputFile(path_or_bytesio='static/trains/train1.png')
            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.reply(
                text=f'За 2 часа сделаете 10 ключевых действий и найдете работу в IT за месяц!\n'
                     '<b>IT Start</b> - это тот самый волшебный пендаль, которого Вам не хватает, чтобы '
                     'уже через неделю пройти минимум 6 собеседований и получить свой первый оффер.',
                parse_mode='HTML')

        case 'hackaton':
            photo_bytes = InputFile(path_or_bytesio='static/trains/train3.png')
            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.reply(
                text=f'Это <u>соревнование для разработчиков, где команды решают задачи по программированию.</u>\n'
                     'Вы опробуете навыки, которые приобрели по ходу курса в условиях реальной разработки.\n'
                     '<b>Цель хакатона</b> — не победа, а обучение. Поэтому выигрывает здесь не только победитель.',
                parse_mode='HTML')

        case 'tech':
            photo_bytes = InputFile(path_or_bytesio='static/trains/train4.png')
            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.reply(
                text=f'За 3 часа мы полностью подготовим любой компьютер для комфортной работы!\n'
                     '<em>Полностью удаленная настройка.</em>\n'
                     'Все что нужно от Вас - установить программу по удаленному доступу',
                parse_mode='HTML')

        # курсы The way
        case 'TheWayPython':
            photo_bytes = InputFile(path_or_bytesio='static/courses/way1.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + str(db2.get_theway_python()) +
                                           f'\n<a href="https://overone.by/thewaypython">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)
            await call.message.delete()

        case 'TheWayEnglish':
            photo_bytes = InputFile(path_or_bytesio='static/courses/way2.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=str(db2.get_theway_eng()) +
                                           f'\n<a href="https://overone.by/thewayenglish">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)
            await call.message.delete()

        case 'TheWayFrontEnd':
            photo_bytes = InputFile(path_or_bytesio='static/courses/way3.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_theway_front() +
                                           f'\n<a href="https://overone.by/thewayfrontend">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'TheWayUIUX':
            photo_bytes = InputFile(path_or_bytesio='static/courses/way4.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_theway_uiux() +
                                           f'\n<a href="https://overone.by/thewayuxui">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'TheWayJava':
            photo_bytes = InputFile(path_or_bytesio='static/courses/way5.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_theway_java() +
                                           f'\n<a href="https://overone.by/thewayjava">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        # курсы Offline
        case 'OfflinePython':
            photo_bytes = InputFile(path_or_bytesio='static/courses/offline1.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_off_python() +
                                           f'\n<a href="https://overone.by/python">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'OfflineFrontEnd':
            photo_bytes = InputFile(path_or_bytesio='static/courses/offline4.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_off_front() +
                                           f'\n<a href="https://overone.by/frontend">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'OfflineUIUX':
            photo_bytes = InputFile(path_or_bytesio='static/courses/offline3.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_off_uiux() +
                                           f'\n<a href="https://overone.by/web-design">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'OfflineJava':
            photo_bytes = InputFile(path_or_bytesio='static/courses/offline2.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_off_java() +
                                           f'\n<a href="https://overone.by/java">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        # курсы Online
        case 'OnlinePython':
            photo_bytes = InputFile(path_or_bytesio='static/courses/online1.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_on_python() +
                                           f'\n<a href="https://overone.by/python_online">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'OnlineFrontEnd':
            photo_bytes = InputFile(path_or_bytesio='static/courses/online4.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.answer(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_on_front() +
                                           f'\n<a https://overone.by/frontend_online">Подробности по ссылке</a>',
                                      parse_mode='HTML', reply_markup=mainMenu)

        case 'OnlineUIUX':
            photo_bytes = InputFile(path_or_bytesio='static/courses/online3.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.reply(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_on_uiux() +
                                          f'\n<a href="https://overone.by/web-design_online">Подробности по ссылке</a>',
                                     parse_mode='HTML', reply_markup=mainMenu)

        case 'OnlineJava':
            photo_bytes = InputFile(path_or_bytesio='static/courses/online2.png')

            await bot.send_photo(chat_id=call.from_user.id, photo=photo_bytes)
            await call.message.reply(text=f'<b>На курсе Вы (научитесь):</b>\n' + db2.get_on_java() +
                                          f'\n<a href="https://overone.by/java_online">Подробности по ссылке</a>',
                                     parse_mode='HTML', reply_markup=mainMenu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
