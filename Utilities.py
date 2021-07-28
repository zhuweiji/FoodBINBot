def create_or_update(data: dict, key, value):
    """ Create a new key:[value] pair in a dictionary if it does not exist,
    otherwise append the new value to the existing key:value pair"""
    try:
        old_values = data.get(key, None)
        if old_values:
            data[key].append(value)
        else:
            data[key] = [value]
        return True

    except Exception:
        return False


def facts_to_str(user_data) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])

def save_to_csv_db(data):
    try:
        with open('csv_db.txt', 'a+') as f:
            f.write(data)
        return 1
    except:
        return -1

# def received_information(update: Update, context: CallbackContext) -> int:
#     """Store info provided by user and ask for the next category."""
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data['choice']
#     user_data[category] = text
#     del user_data['choice']

#     update.message.reply_text(
#         f"Nice! You have added {text} to the list of food! :"
#         f"{facts_to_str(user_data)} You can choose to add more or stop the bot ",
#         reply_markup=markup,
#     )

#     return CHOOSING
