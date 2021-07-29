import logging
import random
import secrets

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    commandhandler, 
    PicklePersistence,
)

from Utilities import *
from models import *
from adding_food import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    pass

def get_all(update: Update, context: CallbackContext) -> int:
    """ get all foodDates stored in a user's user_data and display it"""
    try:
        food_dates = context.user_data.get('FoodDate')
        food_dates = '\n'.join(list(map(str, food_dates)))
        food_dates = food_dates.replace('[','').replace(']','').replace('"','').replace("'",'')
        update.message.reply_text(food_dates)
    except Exception as E:
        print(E)

def randomize(update: Update, context: CallbackContext) -> int:
    try:
        allfood = context.user_data.get('FoodDate')
        random_food = str(random.choice(allfood))
        update.message.reply_text(random_food)
    except Exception as E:
        print(E)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='conversationbot')
    updater = Updater(secrets.get_token(), persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(add_food_conv_handler)
    getall_handler = CommandHandler('getall',get_all)
    random_handler = CommandHandler('randomize',randomize)
    dispatcher.add_handler(getall_handler)
    dispatcher.add_handler(random_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
