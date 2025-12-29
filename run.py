import utils.bot_hub as bot_hub
from time import sleep
import os


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    clear_console()
    if bot_hub.env_exists():
        bot_hub.run_bots()
    else:
        print("\n [!] error: .env doesn't exist, please run setup.py first")


if __name__ == "__main__":
    main()
