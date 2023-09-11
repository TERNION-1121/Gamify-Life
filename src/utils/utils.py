from utils.dbconfig import db 

import datetime
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

    @staticmethod
    def greet() -> None:
        name = db.getUserName()
        current_hour = datetime.datetime.now().hour
        if current_hour >= 0 and current_hour < 12:
            console.print(f"Good Morning {name[0]}!", style="#78FF93")
        elif current_hour >= 12 and current_hour < 16:
            console.print(f"Good Afternoon {name[0]}!", style="#97FFFE")
        elif current_hour > 16 and current_hour < 24:
            console.print(f"Good Evening {name[0]}!", style="#7092DB")

class Application():
    @staticmethod
    def getRank(exp: int) -> str:
        if exp < 100:
            return "[black]Level (I):[/black]\t[cyan italic underline]Neophyte"
        elif exp < 250:
            return "[black]Level (II):[/black]\t[cyan italic underline]Intermediate"
        elif exp < 500:
            return "[black]Level (III):[/black]\t[cyan italic underline]Adept"
        elif exp < 800:
            return "[black]Level (IV):[/black]\t[cyan italic underline]Prime"
        elif exp >= 1200:
            return "[black]Level (V):[/black]\t[cyan italic underline]Paramount"
        
    @staticmethod
    def view_profile():
        console.print("[bold blue underline]Profile", end="\n\n")

        name = ' '.join(db.getUserName())
        exp  = db.getExperiencePts()

        console.print(f"[black]Name:[/black]\t\t[cyan italic underline]{name}")
        console.print(f"{Application.getRank(exp)}")
        console.print(f"[black]Exp. Pts.:[/black]\t{exp}")

    @staticmethod
    def home_screen():
        console.print("[bold blue underline]Home", end="\n\n")
        Utilities.greet()
        console.print("\nReady to take on another challenge?")
        console.print("[black][Press 'P' then 'Enter' to view Profile]\n[Press 'Enter' to start with another goal]")
        inp = console.input()
        while inp.lower() not in " p":
            print("\033[1A\033[2K", end='')
            inp = console.input()
        os.system("clear")
        if inp == "":   # input goal and details
            pass
        elif inp.lower() == 'p':    # go to profile
            Application.view_profile()
        
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