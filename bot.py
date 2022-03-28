import logging
from random import randint

from typing import Dict
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext,)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
CHOOSING, TYPING_REPLY, TYPING_CHOICE, FAQ_REPLY = range(4)

with open('compliments.txt', encoding="utf8") as f:
    compliments = f.readlines()

menu_keyboard = [
    ['Age', 'Favourite colour'],
    ['Number of siblings', 'Compliment'],
    ['FAQ', 'Done'],
]
faq_keyboard = [['Do you still like me?'], ['Am I fat?'], ['Am I ugly?'], ['Am I disgusting?'],['How do I look?']]
faq_answers = ['Yes, he does', 'No you\'re not', 'No you\'re not', 'No you\'re not', 'Stunning as usual']
menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
faq_markup = ReplyKeyboardMarkup(faq_keyboard, one_time_keyboard=True)
really_markup = ReplyKeyboardMarkup([['Really?']], one_time_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
        "Why don't you tell me something about yourself?",
        reply_markup=menu_markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'Your {text.lower()}? Yes, I would love to hear about that!')

    return TYPING_REPLY


def compliment(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        compliments[randint(0,99)]
    )
    print(compliments[randint(0,99)])
    return CHOOSING

def faq(update:Update, context:CallbackContext) -> int:
    """Show FAQ"""
    update.message.reply_text('Please choose a question', reply_markup=faq_markup)

    return FAQ_REPLY

def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    #category = user_data['choice']
    #user_data[category] = text
    faq_questions = faq_keyboard[0]
    if faq_questions[0] == text:
        update.message.reply_text(
            "Yes I do"
        )
    elif faq_questions[2] == text:
        update.message.reply_text(
            "No"
        )

    del user_data['choice']
    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
        " on something.",
        reply_markup=menu_markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1792786927:AAEiCd0d_2jxiGe2vCCQ9NzYOeBWmWKB6wc", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Age|Favourite colour|Number of siblings)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Compliment$'), compliment),
                MessageHandler(Filters.regex('^FAQ$'), faq),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
                )
            ],
            FAQ_REPLY:[
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), received_information, 
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()