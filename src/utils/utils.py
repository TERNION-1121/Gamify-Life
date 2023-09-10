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
    
    os.system("clear")

    home_screen()

def new_comer_screen():
    console.rule("[bold italic blue] Welcome to")
    console.print("[bold blue underline]GAMIFY   LIFE\n\n", justify="center")

    console.input("\t\t\t\t\tReady to lead a [blue underline]life[/blue underline] full of [i]ambitions[/i] and [i]goals[/i]? ")
    print("\033[1A\033[2K", end = '')
    console.print("\t\t\t\t\t\t   Alright! Let's get Started... \n\t\t\t\t\t\t\tWhat's your [i]name[/i]?")

    # Process entered name (error checking sometime later)
    name = console.input("\n\t\t\t\t\t\t[black]Your full name: ")
    name = name.split()
    first_name = name[0]
    if len(name) == 2:
        middle_name = 'NULL'
        last_name = name[1]
    elif len(name) == 3:
        middle_name, last_name = name[1:]
    else:
        middle_name = last_name = 'NULL'

    db.create_tables()
    db.insertUserName(first_name, middle_name, last_name)

    print("\033[4A\033[0J", end = '')
    console.input(f"\t\t\t\t\t\t\tAwesome [blue]{first_name}[/blue]!\n\t\t\t\t\t\tPress [b]Enter[/b] to reach [u]Home Menu[/u].")

def home_screen():
    console.rule("[blue]Home Menu")
    console.print("", justify="right")