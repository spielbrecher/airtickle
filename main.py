import telebot
import config
import ai

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', parse_mode='html')
    bot.send_message(message.chat.id, f'Введите примерное предполагаемое название будущей статьи. Нажмите Ввод.', parse_mode='html')
    bot.send_message(message.chat.id, f'Далее введите примерное описание статьи, пояснения к названию. Нажмите Ввод.', parse_mode='html')

    #bot.send_message(message.chat.id, message)
    config.artickle_name = ''
    config.artickle_synopsis = ''
    config.artickle_description = ''
    config.artickle_hypothesis = ''

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Начните с указания названия статьи и ее описания')

@bot.message_handler()
def info(message):
    if config.artickle_name=='':
        bot.send_message(message.chat.id,'Вероятно, это название статьи. Если нет, то начните заново и введите сначала его')
        config.artickle_name = message.text
    elif config.artickle_synopsis=='':
        bot.send_message(message.chat.id,
                         'Вероятно, это описание статьи. Если нет, то начните заново и введите сначала название, а потом описание статьи')
        config.artickle_synopsis = message.text
    elif message.text.isdigit():
        ai.save_pdf(int(message.text))  # save pdf to drive

    # Формируем гипотезу
    if config.artickle_name and config.artickle_synopsis:
        config.artickle_hypothesis = ai.create_hypothesis()
        bot.send_message(message.chat.id, config.artickle_hypothesis)
        config.artickle_description = \
            f"Название статьи: {config.artickle_name}. Описание статьи: {config.artickle_synopsis} Гипотеза: {config.artickle_hypothesis}"

        # Формируем план написания статьи
        config.plan = ai.create_plan()
        bot.send_message(message.chat.id, config.plan)
    # Формируем ключевые слова
    if config.artickle_description:
        config.keywords = ai.create_ru_keywords()
        bot.send_message(message.chat.id, config.keywords)
        # Формируем ключевые слова на английском языке
        config.translated_keywords = ai.translate_keywords()
        bot.send_message(message.chat.id, config.translated_keywords)

        # Получаем список работ по ключевым словам
        config.literature = ai.get_literature()
        for i, r in enumerate(config.literature):
            bot.send_message(message.chat.id, f"№ {i} - {r.title} - {r}")


bot.polling(none_stop=True)