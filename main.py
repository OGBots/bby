from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace these with your actual details
MY_USERNAME = "SatsNova"  # Your Telegram username
PLANS = {
    "Plan A": "10 USD per month",
    "Plan B": "25 USD per month",
    "Plan C": "50 USD per year"
}

# Simulate a database of users who have subscribed
subscribed_users = {}

# Redeem codes (you can pre-generate these or add dynamically)
redeem_codes = ["OGRedeem270", "OGRedeem269"]

# Function to handle the /start command and show welcome message
def start(update: Update, context: CallbackContext) -> None:
    # Send a welcome message and show available plans
    welcome_message = (
        "Welcome to the OG Subscription Bot!\n\n"
        "Here are the available plans:\n"
        f"1. Plan A: {PLANS['Plan A']}\n"
        f"2. Plan B: {PLANS['Plan B']}\n"
        f"3. Plan C: {PLANS['Plan C']}\n\n"
        "To subscribe, please send your payment proof to the admin. "
        "Once verified, the admin will approve your subscription.\n\n"
        f"For more details, you can contact me: @{SatsNova}"
    )
    update.message.reply_text(welcome_message)

# Function to handle user requests (payment proof or redeem code)
def handle_user_request(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    message = update.message.text.lower()

    # If user asks for a redeem code
    if "redeem" in message:
        update.message.reply_text("Please provide the redeem code to proceed.")
        return

    # Handle invalid message
    update.message.reply_text("I didn't understand your message. Please send your payment proof or redeem code.")

# Function for the admin to approve the user by username
def approve_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.username != MY_USERNAME:
        update.message.reply_text("You do not have permission to approve users.")
        return

    # Extract the username from the command argument
    if context.args:
        username_to_approve = context.args[0]
        user_id_to_approve = None

        # Find the user ID based on the username
        for user_id, username in subscribed_users.items():
            if username == username_to_approve:
                user_id_to_approve = user_id
                break

        if user_id_to_approve:
            subscribed_users[user_id_to_approve] = username_to_approve
            update.message.reply_text(f"User @{username_to_approve} has been approved and is now subscribed!")
        else:
            update.message.reply_text("User not found or not requested redeem code.")

    else:
        update.message.reply_text("Please specify the username to approve.")

# Function to create a redeem code
def create_redeem_code(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.username != MY_USERNAME:
        update.message.reply_text("You do not have permission to create redeem codes.")
        return

    # Generate a new redeem code
    new_code = "REDEEM" + str(len(redeem_codes) + 1)
    redeem_codes.append(new_code)

    update.message.reply_text(f"A new redeem code has been created: {new_code}")

# Function to check if the user has access to the subscription
def check_subscription(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in subscribed_users:
        update.message.reply_text(f"You are subscribed as {subscribed_users[user_id]}")
    else:
        update.message.reply_text("You are not subscribed. Please send your payment proof or request a redeem code.")

# Function to handle user redeem code input
def handle_redeem_code(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    redeem_code = update.message.text.strip()

    if redeem_code in redeem_codes:
        subscribed_users[user_id] = update.message.from_user.username
        update.message.reply_text("Congratulations! You have successfully redeemed your subscription.")
    else:
        update.message.reply_text("Invalid redeem code. Please try again or contact support.")

# Function to show the list of subscribed users (admin use only)
def show_subscribed_users(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.username != MY_USERNAME:
        update.message.reply_text("You do not have permission to view this information.")
        return

    # Display the list of subscribed users
    if subscribed_users:
        update.message.reply_text(f"Subscribed users: {', '.join(subscribed_users.values())}")
    else:
        update.message.reply_text("No users have subscribed yet.")

# Main function to set up the bot
def main():
    # Replace 'YOUR_BOT_API_KEY' with your bot's actual API key
    updater = Updater("8059638176:AAGUZv9bL_cV_3NMj0KWrv1_-xQcF9kCI3c", use_context=True)
    dispatcher = updater.dispatcher

    # Command handler to start the bot
    dispatcher.add_handler(CommandHandler("start", start))

    # Handle user requests for redeem codes or payment proof
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_user_request))

    # Admin commands to approve users and create redeem codes
    dispatcher.add_handler(CommandHandler("approve", approve_user))
    dispatcher.add_handler(CommandHandler("create_redeem_code", create_redeem_code))

    # Command to check subscription status
    dispatcher.add_handler(CommandHandler("check_subscription", check_subscription))

    # Admin command to show the list of subscribed users
    dispatcher.add_handler(CommandHandler("show_subscribed", show_subscribed_users))

    # Handle redeem code input
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_redeem_code))

    # Start polling for new messages
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
