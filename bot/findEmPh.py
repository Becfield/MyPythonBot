import re
import time

import database

from telegram import Update
from telegram.ext import ConversationHandler

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'

def findPhoneNumbers(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(\+7|8)[\- ]?\(?(\d{3})\)?[\- ]?\(?(\d{3})\)?[\- ]?(\d{2})[\- ]?(\d{2})')

    phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов


    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END # Завершаем выполнение функции

    phonesList = []
    for i, groups in enumerate(phoneNumberList):
        phone = f'+7 ({groups[1]}) {groups[2]}-{groups[3]}-{groups[4]}'
        phonesList.append(phone)

    context.user_data['phonesList'] = phonesList

    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i, groups in enumerate(phoneNumberList):
        phone = f'+7 ({groups[1]}) {groups[2]}-{groups[3]}-{groups[4]}'
        phoneNumbers += f'{i+1}. {phone}\n'


    update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
    time.sleep(0.6)
    update.message.reply_text('Хотите сохранить эти номера в базу данных? [Y/n]')
    return 'savePhones_to_db'

def savePhones_to_db(update: Update, context):
    user_response = update.message.text.lower()
    if user_response == 'y':
        # Получаем список номеров телефонов
        phoneNumberList = context.user_data.get('phonesList', [])
        database.funcINSERT('phones', phoneNumberList)
        update.message.reply_text('Номера телефонов успешно сохранены!')
    else:
        update.message.reply_text('Сохранение отменено.')

    return ConversationHandler.END

def findEmailCommand(update: Update, context):
    update.message.reply_text('Закидывай свой текст с email брадка!')

    return 'findEmailBoxes'

def findEmailBoxes(update: Update, context):
    user_input = update.message.text # Получаем текст, содержащий(или нет) mail

    emailBoxRegex = re.compile(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')

    emailBoxList = emailBoxRegex.findall(user_input)  #Ищем почты из сообщения по шаблону

    if not emailBoxList:
        update.message.reply_text('Прости, но здесь нет адресов почт(((')
        return ConversationHandler.END

    emailList = []
    for i in range(len(emailBoxList)):
        emailList.append(emailBoxList[i])

    context.user_data['emailList'] = emailList

    emailBoxes = ''
    for i in range(len(emailBoxList)):
        emailBoxes += f'{i+1}. {emailBoxList[i]}\n'

    update.message.reply_text(emailBoxes)
    time.sleep(0.6)
    update.message.reply_text('Хотите сохранить эти электронные почты в базу данных? [Y/n]')
    return 'saveEmail_to_db'

def saveEmail_to_db(update: Update, context):
    user_response = update.message.text.lower()

    if user_response == 'y':
        emailList = context.user_data.get('emailList', [])
        database.funcINSERT('emails', emailList)
        update.message.reply_text('Электронные почты успешно сохранены!')
    else:
        update.message.reply_text('Сохранение отменено')

    return ConversationHandler.END
