import logging
import random

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, PicklePersistence, CallbackQueryHandler, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Save food
def save_new_food(update: Update, context: CallbackContext) -> None:
    new_food = " ".join(context.args)

    previously_saved_foods = context.user_data.get('saved_foods', None)
    if not previously_saved_foods: # if the user has not saved food before
        context.user_data['saved_foods'] = [new_food]
    else:
        context.user_data['saved_foods'].append(new_food)

    update.message.reply_text(f'Saved new food {new_food}')


# Stages
CHOOSING_CUISINE_STAGE, SELECTION_STAGE = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ],[
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return CHOOSING_CUISINE_STAGE

def choose(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    keyboard =[
        [
            InlineKeyboardButton("5", callback_data=str(FIVE)),
            InlineKeyboardButton("6", callback_data=str(SIX)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    query.edit_message_text(text="Please choose selection", reply_markup=reply_markup)
    return SELECTION_STAGE

def getall(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(context.user_data.get('saved_foods', None))
    return ConversationHandler.END
    

def randomize(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()

    mylist = context.user_data.get('saved_foods', None)

    if mylist is None:
        query.edit_message_text(text = "Please save a food first.")
    else:
        query.edit_message_text(text = random.choice(mylist))
    return ConversationHandler.END

def one(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    cuisine = "1"
    keyboard = [
        [
            InlineKeyboardButton("Get all food", callback_data=str(ONE)),
            InlineKeyboardButton("Randomize", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return SELECTION_STAGE


def two(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    cuisine = "2"
    keyboard = [
        [
            InlineKeyboardButton("Get all food", callback_data=str(ONE)),
            InlineKeyboardButton("Randomize", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return SELECTION_STAGE


def three(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    cuisine = "3"
    keyboard = [
        [
            InlineKeyboardButton("Get all food", callback_data=str(ONE)),
            InlineKeyboardButton("Randomize", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Third CallbackQueryHandler. Choose a route", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SELECTION_STAGE


def four(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    cuisine = "4"
    keyboard = [
        [
            InlineKeyboardButton("Get all food", callback_data=str(ONE)),
            InlineKeyboardButton("Randomize", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return SELECTION_STAGE




def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1917812251:AAGp5dBLVTXyijt3UIysVzwQHIKuXsEjiJM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_CUISINE_STAGE: [
                CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
            ],
            SELECTION_STAGE: [
                CallbackQueryHandler(getall, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(randomize, pattern='^' + str(TWO) + '$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()