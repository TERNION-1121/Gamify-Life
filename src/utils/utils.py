from utils.dbconfig import db 

import os

from rich import print as printc
from rich.console import Console 
console = Console()

class Utilities():
    @staticmethod
    def is_proper_alphabetical_string(string: str):
        alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
        return all(ch in alphabets for ch in string)

    @staticmethod
    def insert_record(item: tuple):
        cur = db.cursor
        cur.execute("INSERT INTO goaldata VALUES(?,?,?,?,?)", item)
        db.commit()

class Application():
    @staticmethod
    def home_screen():
        os.system("cls")

        if db.is_empty():
            Application.new_comer_screen()
            os.system("cls")

        console.print("[bold blue underline]Home")
        console.print("", justify="right")

    @staticmethod
    def new_comer_screen():
        console.print("[bold italic blue]   Welcome to")
        console.print("[bold blue underline]GAMIFY LIFE[/bold blue underline] [italic]~ GLi ~[/italic]", end="\n\n")

        console.input("Ready to lead a [blue underline]life[/blue underline] full of [i]ambitions[/i] and [i]goals[/i]? ")
        print("\033[1A\033[2K", end = '')

        console.print("Alright! Let's get Started...")
        fname = Application.process_name()

        print("\033[2A\033[0J", end = '')
        console.input(f"Awesome [blue]{fname}[/blue]!\nPress [b]Enter[/b] to reach [u]Home Menu[/u]. ")

    @staticmethod
    def process_name():
        name = console.input("What's your [black]full[/black] name? ")
        while not Utilities.is_proper_alphabetical_string(name):
            print("\033[1A\033[2K", end="")
            name = console.input("What's your [black]full[/black] name? [black][Name can only contain alphabets and space][/black] ")

        name = name.split()
        first_name = name[0]
        middle_name = 'NULL'
        last_name = 'NULL'

        if len(name) == 2:
            last_name = name[1]
        elif len(name) == 3:
            middle_name, last_name = name[1:]

        db.create_tables()
        db.insertUserName(first_name, middle_name, last_name)
        return first_name