import telebot
from telebot import types
import gspread

token = '5505175948:AAFxIgjcgcRffiwLXCmOGm8ytu2T-bacbV8'

bot = telebot.TeleBot(token)


# mail = 'admin-418@fuelreservation.iam.gserviceaccount.com'

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id,'Для бронирования отправьте фамилию и сумму (через пробел) \n Минимальная сумма 6000р, шаг 3000р')

# Указываем путь к JSON
gc = gspread.service_account(filename='client_secret.json')
# Открываем тестовую таблицу
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1ikq9euURKrvpQyF4sD-6sE6Rj3vCqjvG4LNiPnMqqNE/edit#gid=0")
# Выводим значение ячейки A1
worksheet = sh.get_worksheet(0)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    surname = message.text.split()[0]
    sum = message.text.split()[1]
    limit = int(worksheet.acell('B1').value)
    currentSum = int(worksheet.acell('B2').value)

    if surname.isalpha():
        if sum.isdigit():
            if int(sum) >= 6000 and int(sum) % 3000 == 0:
                if currentSum >= limit:
                    bot.send_message(message.chat.id, 'Лимит исчерпан')
                elif currentSum + int(sum) > limit and int(sum) > 6000:
                    bot.send_message(message.chat.id, 'Пожалуйста, укажите меньшую сумму, т.к. лимит заканчивается:\nОсталось на сумму' + str(int(limit) - int(currentSum)))
                else:
                    adress = '5'
                    for i in range(5,100):
                        index = 'C' + str(i)
                        adress = str(i)
                        if worksheet.acell(index).value == None:
                            break
                    worksheet.update('A' + adress, message.from_user.username)
                    worksheet.update('B' + adress, surname)
                    worksheet.update('C' + adress, int(sum))
                    bot.send_message(message.chat.id, 'Данные успешно внесены!')
            else:
                bot.send_message(message.chat.id,'Укажите сумму от 6000 с шагом 3000! \nПовторите попытку')
        else:
            bot.send_message(message.chat.id, 'Вторым параметром должна быть сумма(число)\nПовторите попытку')

    else:
        bot.send_message(message.chat.id, 'Первым параметром должна быть фамилия! \nПовторите попытку')


# Запускаем бота
bot.polling(none_stop=True, interval=0)


