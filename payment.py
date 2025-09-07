import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'ref'))
from WalletManager import WalletManager
from config import cfg

wallet_manager = WalletManager(cfg.SEED_PHRASE.split())
TON_ADDRESS = wallet_manager.address

async def generate_payment_comment(amount=1):
    return await wallet_manager.set_expected_transfer(amount)

async def check_payment(comment, min_amount=1):
    payment = await wallet_manager.get_expected_transfer(comment)
    return payment is not None and payment >= min_amount
