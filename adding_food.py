
import logging
import random

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    commandhandler,
)

from Utilities import *
from models import *

CHOOSING, MANUALNAME, MANUALLOCATION, CONFIRM = range(4)

reply_keyboard = [
    ['Link', 'Manually'],
    ['Cancel']
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def savefood(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "Hi! Please choose an option:\n1. Send a link to the bot via google maps or\n2. Type in the name",
        reply_markup=markup,
    )

    return CHOOSING


def link(update: Update, context: CallbackContext) -> str:
    # ['Spago Dining Room', '6688 9955', 'https://maps.app.goo.gl/1qQq8LuT12wq6rzq7']
    users_link = update.message.text.splitlines()
    if len(users_link) == 1:
        name = ""
        location_link = users_link

    elif len(users_link) == 3:
        name = users_link[0]
        location_link = users_link[2]
    else:
        context.bot.send_message(
            chat_id=update.effective_user.id, text=f"Please try another link instead.")

    new_date = FoodDate(name=name, link=location_link)
    successful_update = create_or_update(context.user_data, 'temp', new_date)

    if successful_update:
        context.bot.send_message(
            chat_id=update.effective_user.id, text=f"Saved a new FoodDate {name}")
    else:
        context.bot.send_message(
            chat_id=update.effective_user.id, text='Something went wrong!')

    return CONFIRM

#enter_manual_location


def manual_chosen(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    update.message.reply_text(
        f'Manual entry? Sure! Please enter the location!')

    return MANUALLOCATION


def enter_manual_name(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    create_or_update(context.user_data, 'temp', text)
    update.message.reply_text(f"For the date's location, you have entered {text}")
    update.message.reply_text('Please enter the food:')

    return MANUALNAME

#confirm_or_discard


def enter_manual_location(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    update.message.reply_text(f"For the date's food, you have entered {text}")
    create_or_update(context.user_data, 'temp', text)
    update.message.reply_text(
        "Please press Confirm to save or Cancel to discard",
        reply_markup=ReplyKeyboardMarkup([['Confirm', 'Cancel']], one_time_keyboard=True))

    return CONFIRM


def confirm(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data

    result = user_data.pop('temp', None)
    if result is None:
        update.message.reply_text('Could not retrieve data. Please try again.')

    location = result[0]
    food_name = result[1]
    create_or_update(user_data, 'FoodDate', FoodDate(
        food_name=food_name, location=location))
    update.message.reply_text(f"You have added {location} - {food_name}. Until next time!",
                              reply_markup=ReplyKeyboardMarkup([['Add Another', 'Done']], one_time_keyboard=True))
    text = update.message.text

    return CHOOSING


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f'Finishing up..')
    return ConversationHandler.END


add_food_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('savefood', savefood)],
    states={
        CHOOSING: [
            MessageHandler(Filters.regex(
                '^(Manually|Add Another)$'), manual_chosen),
            MessageHandler(Filters.regex('^(Link)$'), link),
        ],
        MANUALLOCATION: [
            MessageHandler(Filters.regex(
                '^(?!.*[Cc]ancel).*$'), callback=enter_manual_name),
        ],
        MANUALNAME: [
            MessageHandler(Filters.regex(
                '^(?!.*[Cc]ancel).*$'), callback=enter_manual_location),
        ],
        CONFIRM: [
            MessageHandler(Filters.regex(
                '^(?!.*[Cc]ancel).*$'), callback=confirm),
        ]
    },
    fallbacks=[MessageHandler(Filters.regex('([Cc]ancel|Done)'), cancel)],
)
