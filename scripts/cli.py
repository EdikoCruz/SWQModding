#!/usr/bin/env python3


from ast import arg
from os_env import Env
from file_handler import ImpakHandler, ZHandler

import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="SWQModding",
        description="A mod for the game SteamWorld Quest: Hand of Gilgamech."
    )
    parser.add_argument("-i", "--install", help="install mod.", action="store_true")
    parser.add_argument("-u", "--uninstall", help="uninstall mod.", action="store_true")

    env = Env()
    gameFolder = env.get("GAME_FOLDER")
    
    args = parser.parse_args()
    if args.install:
        print("installing...")

        print("unpacking .impak files")
        impakHandler = ImpakHandler(gameFolder)
        impakHandler.unpackAll()

        print("unpacking .z files")
        zHandler = ZHandler(gameFolder)
        zHandler.unpackAll()
    elif args.uninstall:
        print("uninstalling...")

        print("packing .z files")
        zHandler = ZHandler(gameFolder)
        zHandler.packAll()

        print("packing .impak files")
        impakHandler = ImpakHandler(gameFolder)
        impakHandler.packAll()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()