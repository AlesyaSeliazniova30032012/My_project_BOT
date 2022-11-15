from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

import emoji

# кейборд-клавиатура основного меню
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btnCourses = KeyboardButton(text='Обучающие курсы')
btnTrains = KeyboardButton(text='Наши тренинги')
btnTeachers = KeyboardButton(text='Наши преподаватели')
btnLearning = KeyboardButton(text='Об обучении')
btnPartners = KeyboardButton(text='Наши партнеры')
mainMenu.row(btnCourses)
mainMenu.row(btnTeachers, btnPartners)
mainMenu.add(btnLearning, btnTrains)

# инлайн-клавиатура регистрации
registrationNow = InlineKeyboardMarkup(row_width=2)
btnRegistration = InlineKeyboardButton(text=emoji.emojize(':clipboard: Регистрация'), callback_data='RegistrationList')
btnNonRegistration = InlineKeyboardButton(text='Продолжить без регистрации', callback_data='NonRegistration')
btnSite = InlineKeyboardButton(text='Перейти на сайт', url='https://overone.by/')
registrationNow.add(btnRegistration, btnNonRegistration)
registrationNow.row(btnSite)

# кейборд-клавиатура дополнительных возможностей
replyMenu = ReplyKeyboardMarkup(resize_keyboard=True)
btnProfile = KeyboardButton(text='Профиль')
btnSubscribe = KeyboardButton(text='Подписка')
btnSendContact = KeyboardButton(text=emoji.emojize(':telephone_receiver: Поделиться контактом'),
                                request_contact=True)
replyMenu.row(btnProfile)
replyMenu.row(btnSubscribe, btnSendContact)

# инлайн-клавиатура лайков
likeVote = InlineKeyboardMarkup(row_width=2)
btnLike = InlineKeyboardButton(text=emoji.emojize(':thumbs_up:'), callback_data='like')
btnDislike = InlineKeyboardButton(text=emoji.emojize(':thumbs_down:'), callback_data='dislike')
likeVote.add(btnLike, btnDislike)

# инлайн-клавиатура для получения бонусов
playNumb = InlineKeyboardMarkup(row_width=2)
btnRandom = InlineKeyboardButton(text='Показать число, загаданное ботом', callback_data='RandomNumber')
btnDevice = InlineKeyboardButton(text=emoji.emojize(':game_die: Подкинуть кубик'), callback_data='DeviceNumber')
playNumb.add(btnRandom, btnDevice)

# инлайн-клавиатура тренингов
trainList = InlineKeyboardMarkup(row_width=2)
btnStart = InlineKeyboardButton(text='IT "START"', callback_data='ITStart')
btnDetailsStart = InlineKeyboardButton(text=emoji.emojize(':face_with_monocle: Подробнее'),
                                       web_app=WebAppInfo(url='https://overone.by/mainstartit'))
btnHackaton = InlineKeyboardButton(text='Hackaton', callback_data='hackaton')
btnDetailsHackaton = InlineKeyboardButton(text=emoji.emojize(':face_with_monocle: Подробнее'),
                                          web_app=WebAppInfo(url='https://overone.by/mainhackathon'))
btnTech = InlineKeyboardButton(text='Настройка ПК', callback_data='tech')
btnDetailsTech = InlineKeyboardButton(text=emoji.emojize(':face_with_monocle: Подробнее'),
                                      web_app=WebAppInfo(url='https://overone.by/setup'))
trainList.add(btnStart, btnDetailsStart)
trainList.add(btnHackaton, btnDetailsHackaton)
trainList.add(btnTech, btnDetailsTech)

# кейборд-клавиатура обучающих курсов
coursesList = ReplyKeyboardMarkup(resize_keyboard=True)
btnTheWay = KeyboardButton(text='TheWay-обучение')
btnOffline = KeyboardButton(text='Offline-обучение')
btnOnline = KeyboardButton(text='Online-обучение')
coursesList.insert(btnTheWay)
coursesList.insert(btnOffline)
coursesList.insert(btnOnline)

# инлайн-клавиатура курсов The way
courseTheWay = InlineKeyboardMarkup(row_width=3)
btnTheWayPython = InlineKeyboardButton(text='THE WAY PYTHON', callback_data='TheWayPython')
btnTheWayEnglish = InlineKeyboardButton(text='THE WAY ENGLISH', callback_data='TheWayEnglish')
btnTheWayFront = InlineKeyboardButton(text='THE WAY FRONT-END', callback_data='TheWayFrontEnd')
btnTheWayUIUX = InlineKeyboardButton(text='THE WAY UI/UX', callback_data='TheWayUIUX')
btnTheWayJava = InlineKeyboardButton(text='THE WAY JAVA', callback_data='TheWayJava')
courseTheWay.add(btnTheWayPython, btnTheWayJava, btnTheWayEnglish)
courseTheWay.add(btnTheWayUIUX, btnTheWayFront)

# инлайн-клавиатура курсов Offline
courseOffline = InlineKeyboardMarkup(row_width=2)
btnOfflinePython = InlineKeyboardButton(text='OFFLINE PYTHON', callback_data='OfflinePython')
btnOfflineFront = InlineKeyboardButton(text='OFFLINE FRONT-END', callback_data='OfflineFrontEnd')
btnOfflineUIUX = InlineKeyboardButton(text='OFFLINE UI/UX', callback_data='OfflineUIUX')
btnOfflineJava = InlineKeyboardButton(text='OFFLINE JAVA', callback_data='OfflineJava')
courseOffline.add(btnOfflinePython, btnOfflineJava)
courseOffline.add(btnOfflineFront, btnOfflineUIUX)

# инлайн-клавиатура курсов Online
courseOnline = InlineKeyboardMarkup(row_width=2)
btnOnlinePython = InlineKeyboardButton(text='ONLINE PYTHON', callback_data='OnlinePython')
btnOnlineFront = InlineKeyboardButton(text='ONLINE FRONT-END', callback_data='OnlineFrontEnd')
btnOnlineUIUX = InlineKeyboardButton(text='ONLINE UI/UX', callback_data='OnlineUIUX')
btnOnlineJava = InlineKeyboardButton(text='ONLINE JAVA', callback_data='OnlineJava')
courseOnline.add(btnOnlinePython, btnOnlineJava)
courseOnline.add(btnOnlineUIUX, btnOnlineFront)

# генерация случайного логина
passwordGenerate = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btnLogin = KeyboardButton(text='Сгенерировать логин')
passwordGenerate.add(btnLogin)
