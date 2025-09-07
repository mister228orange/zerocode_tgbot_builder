import yaml
import os

class Config:
    def __init__(self, path="secrets.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            secrets = yaml.safe_load(f)
        self.SEED_PHRASE = secrets.get("SEED_PHRASE")
        self.TONCENTER_URL = secrets.get("TONCENTER_URL")
        self.TG_API_ID = secrets.get("TG_API_ID")
        self.TG_API_HASH = secrets.get("TG_API_HASH")
        self.TG_BOT_TOKEN = secrets.get("TG_BOT_TOKEN")

cfg = Config()
