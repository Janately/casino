import telebot
import random

bot = telebot.TeleBot('6660421105:AAEfzMeeNFuhbBqlC3owW9mzcY7s906oHJ4')

balance = 2000
user_stavka = {}  # Словарь для отслеживания ставок пользователей

@bot.message_handler(commands=['start'])
def casino(message):
    global balance
    if balance == 0:
        bot.send_message(message.chat.id, "Пополните баланс, заплатите Эркину 10000 сом наличкой")
    else:
        bot.send_message(message.chat.id, f"{message.from_user.first_name} баланс ({balance}), сделайте ставки в формате 'сумма число', например, '1000 5'. Чтобы завершить ставки, введите /finish.")
        bot.register_next_step_handler(message, process_stavki)

def process_stavki(message):
    global balance
    user_id = message.from_user.id
    if message.text == '/finish':
        if user_id in user_stavka:
            stavki = user_stavka[user_id]['stavki']
            if not stavki:
                bot.send_message(message.chat.id, "Вы не сделали ни одной ставки. Попробуйте снова.")
            else:
                total_winnings = 0
                for stavka in stavki:
                    stavka_sum, number = stavka
                    ranr = random.randint(0, 12)
                    if number == ranr:
                        winnings = stavka_sum * (5 if ranr == 0 else 2)
                        total_winnings += winnings
                        bot.send_message(message.chat.id, f"Ставка {stavka_sum} на число {number} выиграла! Выпало число {ranr}. Ваш выигрыш: {winnings}.")
                    else:
                        bot.send_message(message.chat.id, f"Ставка {stavka_sum} на число {number} проиграла. Выпало число {ranr}.")
                balance += total_winnings
                bot.send_message(message.chat.id, f"Итого ваш выигрыш: {total_winnings}. Ваш баланс: {balance}.")
                del user_stavka[user_id]
                bot.send_message(message.chat.id, "Желаете сделать еще ставку? Введите /start")
        else:
            bot.send_message(message.chat.id, "Вы не сделали ни одной ставки. Попробуйте снова.")
    else:
        try:
            text = message.text.split()
            if len(text) != 2:
                raise ValueError
            stavka_sum = int(text[0])
            number = int(text[1])
            if stavka_sum <= balance:
                if user_id not in user_stavka:
                    user_stavka[user_id] = {'stavki': []}
                user_stavka[user_id]['stavki'].append((stavka_sum, number))
                bot.send_message(message.chat.id, f"Вы сделали ставку {stavka_sum} на число {number}.")
            else:
                bot.send_message(message.chat.id, "Ваша ставка превышает баланс.")
        except (ValueError, IndexError):
            bot.send_message(message.chat.id, "Некорректный формат ставки. Введите сумму и число через пробел, например, '1000 5'.")

bot.polling(none_stop=True)
