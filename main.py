import asyncio
from typing import List, Dict

from telethon import TelegramClient, events, Button
from models import Graph, Node

nodes: List[Node] = [
    Node(0, ''),
    Node(1, 'Отправить отчет'),
    Node(2, 'Монтаж'),
    Node(3, 'пусконаладка'),
    Node(4, 'Sharazh'),
    Node(5, 'KHC'),
    Node(6, 'Кабель'),
    Node(7, 'Оборудование'),
    Node(8, '5е'),
    Node(9, '6е'),
    Node(10, 'Оптоволокно'),
    Node(11, 'Прочее'),
    Node(12, 'Камеры'),
    Node(13, 'Заявка')
]

graph = {
    0: [1, 13],
    1: [2, 3, 4],
    2: [5, 6, 7, 11],
    6: [8, 9, 10],
    7: [12]
}
adjacency_list = [[] for i in range(14)]
for line in graph:
    adjacency_list[line] = graph[line]

for parent, childs in graph.items():
    print(parent, childs)
    nodes[parent].childs = [nodes[child] for child in childs]

api_id = '27692732'  # Replace with your API ID
api_hash = 'cca60cccebac74004a31fec133c9c275'  # Replace with your API Hash
bot_token = '8422407349:AAFhjKak7-dd_sYbaGNKHGMPPalhQK32CM0'  # Replace with your Bot Token

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)


class Menu:
    def __init__(self, graph: Graph, entry_point: Node):
        self.graph = graph
        self.cur, self.prev = entry_point, None

    def choose(self, node_number: int):
        self.prev = self.cur
        self.cur = node_number
        self.current_options: Dict[Node: List[Node]] = [[Button.inline(child.title, child.id)] for child in nodes[node_number].childs] + \
                     [([Button.inline("Назад", node_number)] * node_number)[:1]]

    def get_buttons(self):
        return self.current_options

menu = Menu()

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    menu.choose(0)
    await event.respond(
        "Welcome! Please choose an option:",
        buttons=menu.get_buttons()
    )


@client.on(events.CallbackQuery)
async def callback_handler(event):
    print(event, int(event.data))
    k = int(event.data)
    await event.answer(f"You selected {nodes[k].title}.")
    menu.choose(int(event.data))
    await event.edit(
        f"Выберете тип исполненных работ:{k}",
        buttons=menu.choose(int(event.data))
    )


print("Bot is running...")
client.run_until_disconnected()
