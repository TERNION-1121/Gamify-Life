from utils.dbconfig import db 

import os

from rich import print as printc
from rich.console import Console 
console = Console()

def insert_record(item: tuple):
    cur = db.cursor
    cur.execute("INSERT INTO goaldata VALUES(?,?,?,?,?)", item)
    db.commit()

def welcome_screen():
    os.system("clear")

    if db.is_empty():
        new_comer_screen()

def new_comer_screen():
    console.rule("[bold italic blue] Welcome to")
    console.print("[bold blue underline]GAMIFY   LIFE\n\n", justify="center")

    console.input("\t\t\t\t\tReady to lead a [blue underline]life[/blue underline] full of [i]ambitions[/i] and [i]goals[/i]? ")
    print("\033[1A\033[2K", end = '')
    console.print("\t\t\t\t\t\t   Alright! Let's get Started... \n\t\t\t\t\t\t\tWhat's your [i]name[/i]?")

    name = console.input("\n\t\t\t\t\t\t[black]Your full name: ")
    first_name, last_name = name.split()
    print("\033[4A\033[0J", end = '')
    console.input(f"Awesome {first_name}!")