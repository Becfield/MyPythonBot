import os, logging, psycopg2

from psycopg2 import Error
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ConversationHandler

# Подключаем файл .env
load_dotenv()

logging.basicConfig(
    filename='app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, encoding="utf-8"
)

#Подключение к БД
def ConnectionOpen():
    try:
        connection = psycopg2.connect(user=f"{os.getenv('DB_USER')}",
                                          password=f"{os.getenv('DB_PASSWORD')}",
                                          host=f"{os.getenv('DB_HOST')}",
                                          port="5432",
                                          database=f"{os.getenv('DB_DATABASE')}")

        cursor = connection.cursor()
        logging.info("Подключение успешно произведено")
        return connection, cursor
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    return None, None

# Отключение от базы данных
def CloseConnection():
    connection, cursor = ConnectionOpen()
    if connection is not None:
        cursor.close()
        connection.close()

def funcSELECT(table):
    connection, cursor = ConnectionOpen()
    # Выполнение SELECT
    cursor.execute(f"SELECT * FROM {table};")
    data = cursor.fetchall()
    for row in data:
        print(row)
    logging.info("Команда SELECT успешно выполнена")
    CloseConnection()
    return data

# Вывод пользователю данных в таблице emails
def getEmails(update: Update, context):
    command = 'emails'
    emailsList = funcSELECT(command)
    emails = ''
    for email in emailsList:
        emails += f'{email[0]}. {email[1]}\n'
    update.message.reply_text(emails)
    return ConversationHandler.END

# Вывод пользователю данных в таблице phones
def getPhones(update: Update, context):
    command = 'phones'
    phoneList = funcSELECT(command)
    phones = ''
    for phone in phoneList:
        phones += f'{phone[0]}. {phone[1]}\n'
    update.message.reply_text(phones)

    return ConversationHandler.END


def funcINSERT(table, values):
    connection, cursor = ConnectionOpen()
    sql_values = ", ".join(["('" + str(value) + "')" for value in values])
    # Выполнение INSERT
    if table == 'phones':
        cursor.execute(f"INSERT INTO {table} (phone_number) VALUES {sql_values};")
        connection.commit()
        logging.info("Команда INSERT успешно выполнена. Данные записаны в phones")

    elif table == 'emails':
        cursor.execute(f"INSERT INTO {table} (email) VALUES {sql_values};")
        connection.commit()
        logging.info("Команда INSERT успешно выполнена. Данные записаны в emails")

    CloseConnection()



