import os
import random
from telethon import TelegramClient, events, Button
from db import set_user_state, get_user_state
from payment import TON_ADDRESS, generate_payment_comment, check_payment

api_id = os.getenv('TG_API_ID') or '27692732'
api_hash = os.getenv('TG_API_HASH') or 'cca60cccebac74004a31fec133c9c275'
bot_token = os.getenv('TG_BOT_TOKEN') or '8422407349:AAFhjKak7-dd_sYbaGNKHGMPPalhQK32CM0'
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    user_id = event.sender_id
    intro = (
        "🤖 <b>Zerocode Telegram Bot Builder</b>\n\n"
        "1. Describe your workflow in draw.io and export as XML.\n"
        "2. Upload the XML here.\n"
        "3. Pay 1 TON to generate your custom Telegram bot.\n"
        "4. Receive a ready-to-run Go executable in a zip archive!\n\n"
        "Choose an option below:"
    )
    buttons = [
        [Button.inline("About", b"about")],
        [Button.inline("Create Bot", b"create")]
    ]
    await event.respond(intro, buttons=buttons, parse_mode="html")

@client.on(events.CallbackQuery(pattern=b"about"))
async def about_handler(event):
    await event.answer()
    await event.respond(
        "<b>About:</b>\nThis service lets you create a Telegram bot from a draw.io workflow (XML). "
        "After payment, you get a Go executable in a zip archive, ready to deploy!\n\n"
        "Use /start to return to the main menu.",
        parse_mode="html"
    )

@client.on(events.CallbackQuery(pattern=b"create"))
async def create_handler(event):
    user_id = event.sender_id
    await event.answer()
    await event.respond(
        "Please upload your workflow XML file exported from draw.io."
    )
    await set_user_state(user_id, state="awaiting_xml")

@client.on(events.NewMessage(func=lambda e: e.file and e.file.name.endswith('.xml')))
async def handle_xml_file(event):
    user_id = event.sender_id
    state = await get_user_state(user_id)
    if not state or state.get("state") != "awaiting_xml":
        await event.respond("Please use /start and choose 'Create Bot' first.")
        return
    file_name = f"user_{user_id}_{random.randint(1000,9999)}.xml"
    file_path = os.path.join(os.getcwd(), file_name)
    await event.download_media(file=file_path)
    comment = await generate_payment_comment(1)
    await set_user_state(user_id, xml=file_path, state="awaiting_payment", paid=False, comment=comment)
    await event.respond(f"XML received! To generate your bot, please pay 1 TON to this address:\n<code>{TON_ADDRESS}</code>\nWith comment: <code>{comment}</code>\nAfter payment, send /paid.", parse_mode="html")

@client.on(events.NewMessage(pattern='/paid'))
async def handle_paid(event):
    user_id = event.sender_id
    state = await get_user_state(user_id)
    if not state or not state.get("xml") or state.get("state") != "awaiting_payment":
        await event.respond("No XML file found or wrong step. Please use /start and follow the steps.")
        return
    comment = state.get("comment")
    if not comment:
        await event.respond("No payment comment found. Please re-upload your XML.")
        return
    paid = await check_payment(comment, 1)
    if paid:
        await set_user_state(user_id, paid=True, state="ready")
        zip_path = os.path.join(os.getcwd(), "go_bot_project.zip")
        if os.path.exists(zip_path):
            await event.respond("Payment received! Here is your generated Go Telegram bot (executable in zip):", file=zip_path)
        else:
            await event.respond("Payment received! (But zip archive not found on server.)")
    else:
        await event.respond("Payment not found or not confirmed yet. Please wait a few minutes and try again.")
