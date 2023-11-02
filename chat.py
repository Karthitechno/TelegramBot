import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Define conversation states
SELECTING_QUESTION, ANSWERING_QUESTION = range(2)

# Define custom keyboard options
reply_keyboard = [['Yes', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# Define the questions and answers for insomnia detection
questions = [
    "Do you have difficulty falling asleep?",
    "Do you wake up multiple times during the night?",
    "Do you have trouble staying asleep?",
    "Do you wake up too early and can't go back to sleep?",
    "Do you feel tired or fatigued during the day?",
    "Do you have difficulty concentrating?",
    "Do you have irritability or mood swings?",
    "Do you experience anxiety or restlessness before bedtime?",
    "Do you use electronics or screen devices close to bedtime?",
    "Do you consume caffeine or stimulants close to bedtime?",
    "Do you engage in vigorous physical activity close to bedtime?",
    "Do you nap excessively during the day?",
    "Do you have a regular sleep schedule?",
    "Do you sleep in a comfortable and quiet environment?",
    "Do you have a bedtime routine that helps you relax?",
    "Do you have a comfortable mattress and pillow?",
    "Do you avoid large meals or heavy snacks close to bedtime?",
    "Do you avoid alcohol or nicotine close to bedtime?",
    "Do you have any underlying medical conditions affecting sleep?",
    "Do you take any medications that may disrupt sleep?",
    "Do you experience any pain or discomfort while trying to sleep?",
    "Do you have any sleep disorders such as sleep apnea or restless leg syndrome?",
    "Do you have a high level of stress or anxiety in your life?",
    "Do you have a history of insomnia in your family?",
    "Do you feel refreshed after waking up in the morning?",
    "Do you feel rested and restored after a night's sleep?",
    "Do you have difficulty staying awake during the day?",
    "Do you have nightmares or vivid dreams during sleep?",
    "Do you experience a racing heart or palpitations during sleep?",
    "Do you have a consistent sleep-wake schedule?",
    "Do you avoid bright lights or electronic screens before bedtime?",
    "Do you have a comfortable and supportive sleep environment?",
    "Do you engage in relaxation techniques before bedtime?",
    "Do you avoid napping during the day?",
    "Do you limit your caffeine intake?",
    "Do you avoid heavy meals or snacks close to bedtime?",
    "Do you engage in regular physical exercise?",
    "Do you manage your stress levels effectively?",
    "Do you practice good sleep hygiene?",
    "Do you seek professional help for sleep problems?",
    "Do you have a quiet and dark bedroom?",
    "Do you avoid clock-watching while in bed?",
    "Do you use your bed only for sleep and intimacy?",
    "Do you expose yourself to natural light during the day?",
    "Do you have a wind-down routine before bedtime?",
    "Do you use relaxation techniques to help you sleep?",
    "Do you keep a sleep diary to track your sleep patterns?",
    "Do you avoid using electronic devices in bed?",
    "Do you limit your fluid intake before bedtime?",
    "Do you sleep in a well-ventilated room?",
    "Do you maintain a cool temperature in your bedroom?",
    "Do you practice meditation or mindfulness before bed?",
    "Do you avoid stimulating activities before bed?",
    "Do you have a regular wake-up time?",
    "Do you avoid working or studying in bed?",
    "Do you avoid exposure to loud noises during sleep?",
    "Do you practice stress-reducing activities during the day?",
]

# Define the threshold for insomnia diagnosis
INSOMNIA_THRESHOLD = 35


def start(update, context):
    update.message.reply_text(
        "Welcome to the Insomnia Detection Bot! I'm here to help you determine if you have symptoms of insomnia."
        "Please answer a few questions. Let's begin!"
    )
    return ask_question(update, context)


def ask_question(update, context):
    user_data = context.user_data

    if 'current_question' not in user_data:
        user_data['current_question'] = 0

    current_question = user_data['current_question']

    if current_question >= len(questions):
        return finish_quiz(update, context)

    update.message.reply_text(questions[current_question], reply_markup=markup)
    return ANSWERING_QUESTION


def record_answer(update, context):
    user_data = context.user_data
    current_question = user_data['current_question']

    answer = update.message.text
    user_data[current_question] = answer.lower()

    user_data['current_question'] += 1
    return ask_question(update, context)


def finish_quiz(update, context):
    user_data = context.user_data

    score = sum(1 for q in questions if user_data.get(q, '').lower() == 'yes')

    if score >= INSOMNIA_THRESHOLD:
        diagnosis = "Based on your answers, it appears that you may have symptoms of insomnia. It is recommended to consult a healthcare professional for further evaluation and guidance."
    else:
        diagnosis = "Based on your answers, it does not appear that you have symptoms of insomnia. However, if you continue to experience sleep difficulties, it is advisable to seek medical advice."

    update.message.reply_text(diagnosis, reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text("Quiz canceled.", reply_markup=ReplyKeyboardRemove())
    user_data = context.user_data
    user_data.clear()
    return ConversationHandler.END


def main():
    # Create the Updater and dispatcher
    updater = Updater("5844372448:AAHNQVuzPMw5TDRc4845PqlFEWmDzLr6PGQ")
    dispatcher = updater.dispatcher

    # Create the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_QUESTION: [
                MessageHandler(Filters.regex('^Yes$|^No$'), record_answer)
            ],
            ANSWERING_QUESTION: [
                MessageHandler(Filters.regex('^Yes$|^No$'), record_answer)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the dispatcher
    dispatcher.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
