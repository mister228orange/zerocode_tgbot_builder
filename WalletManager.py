import asyncio
import json
import aiohttp
from tonutils.client import ToncenterClient
from tonutils.wallet import WalletV5R1
from tonsdk.utils import to_nano
from tonsdk.boc import Cell
from tonsdk.utils import Address
from random import randint
from config import cfg

class WalletManager:
    def __init__(self, seed_phrase):
        self.client = ToncenterClient(is_testnet=False)
        self.wallet, self.public_key, self.private_key, self.mnemonic = WalletV5R1.from_mnemonic(self.client, seed_phrase)
        self.expected_transfers = {}
        self.address = self.wallet.address.to_str(True, True)

    async def simple_send_ton(self, to_address: str, amount: float, comment=''):
        print(f"Start to send from {self.wallet} to {to_address} {amount} Tons")
        balance = await self.wallet.get_balance(self.client, self.address)
        await asyncio.sleep(2)
        print(f"[+] Баланс: {balance / 1e9} TON")
        amount_nano = to_nano(amount, "ton")
        if balance < amount_nano:
            print("[-] Недостаточно средств")
            return
        seqno = await self.wallet.get_seqno(self.client, self.address)
        await asyncio.sleep(2)
        print(f'seqneunce number is {seqno}')
        transfer = await self.wallet.transfer(
            destination=to_address,
            amount=amount,
            body=comment
        )
        print(transfer)

    async def get_estimated_fees(self, message_boc: str):
        url = 'https://toncenter.com/api/v2/estimateFee'
        params = {
            'body': message_boc,
            'address': self.wallet.address.to_str(True, True),
            'boc': message_boc
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as resp:
                data = await resp.json()
                return data

    async def set_expected_transfer(self, amount):
        while 1:
            code = str(randint(100,10000000))
            if code in self.expected_transfers:
                continue
            self.expected_transfers[code] = -amount
            return code

    async def get_expected_transfer(self, code):
        print(f'Transfer with code {code} status: {self.expected_transfers.get(code)}')
        return self.expected_transfers.get(code)

    async def remove_expected_transfer(self, code):
        self.expected_transfers.pop(code)

    async def check_payments(self, interval):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    params = {
                        'address': self.wallet.address.to_str(is_user_friendly=False),
                        'limit': 10,
                        'to_lt': 0
                    }
                    async with session.get(cfg.TONCENTER_URL + 'getTransactions', params=params) as resp:
                        txt = await resp.text()
                        data = json.loads(txt)
                        if not data.get("ok"):
                            print("❌ Ошибка при запросе к TonCenter:", data)
                            await asyncio.sleep(interval)
                            continue
                        transactions = data.get("result", [])
                        for tx in transactions:
                            in_msg = tx.get("in_msg", {})
                            if not in_msg:
                                continue
                            msg_value = int(in_msg.get("value", 0)) / 1e9  # Переводим в TON
                            code = in_msg.get("message", "")
                            if code in self.expected_transfers:
                                self.expected_transfers[code] += msg_value
                                print(f"✅ Найден платёж: {msg_value} TON, комментарий: '{code}'")
                                return tx  # Или return True
                await asyncio.sleep(interval)
            except Exception as e:
                print("⚠️ Ошибка в проверке TON платежа:", e)
                await asyncio.sleep(interval)

    async def estimated_fees_send_ton(self, to_address: str, amount: float, comment=''):
        print(f"Start to send from {self.wallet} to {to_address} {amount} TON")
        balance = await self.wallet.get_balance(self.client, self.address)
        await asyncio.sleep(1)
        print(f"[+] Баланс: {balance / 1e9:.8f} TON")
        amount_nano = to_nano(amount, "ton")
        # Создаём тело сообщения с комментарием
        body = Cell()
        body.bits.write_bytes(comment.encode('utf-8'))
        # Сначала создаём сообщение для оценки газа
        msg = self.wallet.create_internal_msg(
            dest=Address(to_address),
            value=amount_nano,
            body=body
        )
        boc = msg.serialize().to_boc(False)
        fees = await self.get_estimated_fees(boc)
        total_fee = fees.gas_fee + fees.fwd_fee
        print(f"[+] Estimated fee: {total_fee / 1e9:.6f} TON")
        total_amount = amount_nano + total_fee
        if balance < total_amount:
            print("[-] Недостаточно средств с учётом комиссии")
            return
        # Выполняем перевод
        transfer = await self.wallet.transfer(
            destination=to_address,
            amount=total_amount,
            body=body
        )
        print(f"[+] Transfer result: {transfer}")
