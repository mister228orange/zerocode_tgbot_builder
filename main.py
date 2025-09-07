
import asyncio
from telethon import TelegramClient, events, Button
from models import Graph, Node, Edge
from xml2graph import xml2graph
from xml.etree.ElementTree import ElementTree

# --- Load graph from XML ---
xml_path = "graph.xml"
xml_tree = ElementTree(file=xml_path)
graph: Graph = xml2graph(xml_tree)

# --- Telethon bot config ---
api_id = '27692732'  # Replace with your API ID
api_hash = 'cca60cccebac74004a31fec133c9c275'  # Replace with your API Hash
bot_token = '8422407349:AAFhjKak7-dd_sYbaGNKHGMPPalhQK32CM0'  # Replace with your Bot Token
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# --- Helper: get children for a node ---
def get_children(graph: Graph, node: Node):
    return [edge.target for edge, _ in graph.adj_list.get(node, [])]

# --- Helper: get node by id ---
def get_node_by_id(graph: Graph, node_id: int):
    for node in graph.nodes:
        if node and node.id == node_id:
            return node
    return None


# --- SQLite stateful storage ---
import aiosqlite
DB_PATH = os.path.join(os.getcwd(), "user_states.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_state (
                tgid INTEGER PRIMARY KEY,
                state TEXT,
                xml TEXT,
                paid INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def set_user_state(tgid, state=None, xml=None, paid=None):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT tgid FROM user_state WHERE tgid=?", (tgid,))
        exists = await cur.fetchone()
        if exists:
            if state is not None:
                await db.execute("UPDATE user_state SET state=? WHERE tgid=?", (state, tgid))
            if xml is not None:
                await db.execute("UPDATE user_state SET xml=? WHERE tgid=?", (xml, tgid))
            if paid is not None:
                await db.execute("UPDATE user_state SET paid=? WHERE tgid=?", (int(paid), tgid))
        else:
            await db.execute("INSERT INTO user_state (tgid, state, xml, paid) VALUES (?, ?, ?, ?)", (tgid, state or '', xml or '', int(paid) if paid is not None else 0))
        await db.commit()

async def get_user_state(tgid):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT state, xml, paid FROM user_state WHERE tgid=?", (tgid,))
        row = await cur.fetchone()
        if row:
            return {"state": row[0], "xml": row[1], "paid": bool(row[2])}
        return None



# --- Step 1: Intro message with buttons ---
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

# --- Step 2: About and Create Bot button handlers ---
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

async def send_node(event, node: Node):
    # Get children
    children = [edge[1] for edge in graph.adj_list.get(node, [])]
    if not children:
        await event.respond(f"{node.value[0] if node.value else 'Конец'}\n(leaf node)")
        return
    buttons = [Button.inline(child.value[0] if child.value else str(child.id), str(child.id)) for child in children]
    await event.respond(node.value[0] if node.value else str(node.id), buttons=buttons)

@client.on(events.CallbackQuery)
async def callback_handler(event):
    user_id = event.sender_id
    node_id = int(event.data)
    node = get_node_by_id(graph, node_id)
    if node:
        await set_user_state(user_id, state=str(node_id))
        await send_node(event, node)
    else:
        await event.answer("Node not found.", alert=True)


# --- File upload, payment, and bot generation logic ---

import os
import random
import sys
sys.path.append(os.path.join(os.getcwd(), 'ref'))
from WalletManager import WalletManager
from config import cfg


# --- TON WalletManager setup ---
wallet_manager = WalletManager(cfg.SEED_PHRASE.split())
TON_ADDRESS = wallet_manager.address




@client.on(events.NewMessage(func=lambda e: e.file and e.file.name.endswith('.xml')))
async def handle_xml_file(event):
    user_id = event.sender_id
    state = await get_user_state(user_id)
    if not state or state.get("state") != "awaiting_xml":
        await event.respond("Please use /start and choose 'Create Bot' first.")
        return
    # Save uploaded XML
    file_name = f"user_{user_id}_{random.randint(1000,9999)}.xml"
    file_path = os.path.join(os.getcwd(), file_name)
    await event.download_media(file=file_path)
    # Generate unique comment for payment
    comment = await wallet_manager.set_expected_transfer(1)
    await set_user_state(user_id, xml=file_path, state="awaiting_payment", paid=False)
    await set_user_state(user_id, state="awaiting_payment", xml=file_path, paid=False)
    await set_user_state(user_id, state="awaiting_payment", xml=file_path, paid=False, comment=comment)
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
    # Check payment for this comment
    payment = await wallet_manager.get_expected_transfer(comment)
    if payment is not None and payment >= 1:
        await set_user_state(user_id, paid=True, state="ready")
        zip_path = os.path.join(os.getcwd(), "go_bot_project.zip")
        if os.path.exists(zip_path):
            await event.respond("Payment received! Here is your generated Go Telegram bot (executable in zip):", file=zip_path)
        else:
            await event.respond("Payment received! (But zip archive not found on server.)")
    else:
        await event.respond("Payment not found or not confirmed yet. Please wait a few minutes and try again.")



import asyncio
from db import init_db
from bot import client

async def main():
    await init_db()
    print("Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
