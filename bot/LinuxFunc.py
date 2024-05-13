import os, paramiko
import time
from telegram import Update
from telegram.ext import ConversationHandler

# Функция подключения SSH
def sshConnect(command):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(f'{command}')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]

    return data

# Сбор информации о системе о релизе:
def getRelease(update: Update, context):
    update.message.reply_text(f'{sshConnect("lsb_release -a")}')

# Сбор информации о системе, об архитектуры процессора, имени хоста системы и версии ядра
def getUname(update: Update, context):
    update.message.reply_text(f'{sshConnect("uname -m")} {sshConnect("hostname")} {sshConnect("uname -r")}')

# Сбор информации о времени работы
def getUptime(update: Update, context):
    update.message.reply_text(f'{sshConnect("uptime")}')

# Сбор информации о состоянии оперативной памяти
def getFree(update: Update, context):
    update.message.reply_text(f'{sshConnect("free -h")}')

# Сбор информации о производительности системы
def getMpstat(update: Update, context):
    update.message.reply_text(f'{sshConnect("mpstat")}')

# Сбор информации о работающих в данной системе пользователях.
def getW(update: Update, context):
    update.message.reply_text(f'{sshConnect("who")}')

# Сбор логов. Последние 10 входов в систему
def getAuths(update: Update, context):
    update.message.reply_text(f'{sshConnect("last -n 10")}')

# Сбор логов. Последние 5 критических событий
def getCritical(update: Update, context):
    update.message.reply_text(f'{sshConnect("journalctl -p crit -n 5")}')

# Сбор информации о запущенных процессах
def getPs(update: Update, context):
    update.message.reply_text(f'{sshConnect("ps")}')

# Сбор информации об используемых портах
def getSs(update: Update, context):
    update.message.reply_text(f'{sshConnect("netstat -tuln")}')

# Сбор информации об установленных пакетах
def getAptListCommand(update: Update, context):
    update.message.reply_text('Что вы хотите? Введите число\n'
                              '1. Вывести информацию обо всех пакетах.\n'
                              '2. Введите имя определённого пакета')
    return 'getAptListPackets'

def getAptListPackets(update: Update, context):
    user_input = update.message.text

    if (user_input == '1'):
        packages_info = sshConnect("dpkg -l")
        if packages_info:
            lines = packages_info.strip().split('\n')
            # Отправляем каждую строку в отдельном сообщении
            for i in range(0, len(lines), 20):
                time.sleep(1)
                update.message.reply_text('\n'.join(lines[i:i + 20]))
        else:
            update.message.reply_text('Не удалось получить информацию о пакетах.')
    elif (user_input == '2'):
        update.message.reply_text('Введите название пакета')
        return 'getPacketName'
    else:
        update.message.reply_text('Введите корректное число!')

    return ConversationHandler.END

def getPacketName(update: Update, context):
    package_name = update.message.text
    package_info = sshConnect(f"dpkg-query -l {package_name}")
    if package_info:
        update.message.reply_text(package_info)
    else:
        update.message.reply_text('Пакет не найден. Попробуйте ещё раз.')
    return ConversationHandler.END

# Сбор информации о запущенных сервисах
def getServices(update: Update, context):
    services_info = sshConnect("systemctl list-units")
    if services_info:
        lines = services_info.strip().split('\n')
        # Отправляем каждую строку в отдельном сообщении
        for i in range(0, len(lines), 20):
            time.sleep(1)
            update.message.reply_text('\n'.join(lines[i:i + 20]))
    else:
        update.message.reply_text('Не удалось получить информацию о пакетах.')


def getReplLogs(update: Update, context):
    command = 'grep -E \"repl_user|database\" /var/log/postgresql/postgresql-15-main.log'
    logs_info = sshConnect(command)
    if logs_info:
        lines = logs_info.strip().split('\n')
        # Отправляем каждую строку в отдельном сообщении
        for i in range(0, len(lines), 20):
            time.sleep(1)
            update.message.reply_text('\n'.join(lines[i:i + 20]))
    else:
        update.message.reply_text('Логи не найдены.')
