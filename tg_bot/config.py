import os


class BotConfig:
    BOT_TOKEN = os.getenv("BOT_TOKEN")


bot_config = BotConfig()
