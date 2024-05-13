import logging, os, re

import LinuxFunc, database, findEmPh

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Подключаем файл .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')

#Проверка пароля на сложность
def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Отправь мне свой пароль, только надёжный')
    return 'verifyPasswordProcess'

def verifyPasswordProcess(update: Update, context):
    user_input = update.message.text # Получаем текст содержащий пароль

    verifyPasswordRegex = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}') # Задаём условие отбора надежного пароля

    verifyPasswordCheck = verifyPasswordRegex.search(user_input) # Берём пароль пользователя и проверяем

    if verifyPasswordCheck:
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой. Попробуй ещё раз.')
        return
    return ConversationHandler.END


def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandler = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findEmPh.findPhoneNumbersCommand),
                      CommandHandler('find_email', findEmPh.findEmailCommand),
                      CommandHandler('verify_password', verifyPasswordCommand),
                      CommandHandler('get_apt_list', LinuxFunc.getAptListCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findEmPh.findPhoneNumbers)],
            'findEmailBoxes': [MessageHandler(Filters.text & ~Filters.command, findEmPh.findEmailBoxes)],
            'verifyPasswordProcess': [MessageHandler(Filters.text & ~Filters.command, verifyPasswordProcess)],
            'getAptListPackets': [MessageHandler(Filters.text & ~Filters.command, LinuxFunc.getAptListPackets)],
            'getPacketName': [MessageHandler(Filters.text & ~Filters.command, LinuxFunc.getPacketName)],
            'savePhones_to_db': [MessageHandler(Filters.text & ~Filters.command, findEmPh.savePhones_to_db)],
            'saveEmail_to_db': [MessageHandler(Filters.text & ~Filters.command, findEmPh.saveEmail_to_db)],
        },
        fallbacks=[]
    )

    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandler)
    dp.add_handler(CommandHandler("get_release", LinuxFunc.getRelease))
    dp.add_handler(CommandHandler("get_uname", LinuxFunc.getUname))
    dp.add_handler(CommandHandler("get_uptime", LinuxFunc.getUptime))
    dp.add_handler(CommandHandler("get_free", LinuxFunc.getFree))
    dp.add_handler(CommandHandler("get_mpstat", LinuxFunc.getMpstat))
    dp.add_handler(CommandHandler("get_w", LinuxFunc.getW))
    dp.add_handler(CommandHandler("get_auths", LinuxFunc.getAuths))
    dp.add_handler(CommandHandler("get_critical", LinuxFunc.getCritical))
    dp.add_handler(CommandHandler("get_ps", LinuxFunc.getPs))
    dp.add_handler(CommandHandler("get_ss", LinuxFunc.getSs))
    dp.add_handler(CommandHandler("get_services", LinuxFunc.getServices))
    dp.add_handler(CommandHandler("get_repl_logs", LinuxFunc.getReplLogs))
    dp.add_handler(CommandHandler("get_emails", database.getEmails))
    dp.add_handler(CommandHandler("get_phone_numbers", database.getPhones))


    # Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()