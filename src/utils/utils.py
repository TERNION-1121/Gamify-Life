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
    GOAL_TYPES = ["Academic", "Sports", "Self-Oriented", "Work/Skill-Oriented", "Others"]
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
    def new_goal():
        console.print("[bold blue underline]New Goal", end="\n\n")

        console.print("Hurray!")
        console.print("Let's get started with this...")
        console.print("Enter the number, which most suitably describes your [u]Goal Type[/u]:-")
        console.print("\t1. Academic")
        console.print("\t2. Sports")
        console.print("\t3. Self-Oriented")
        console.print("\t4. Work/Skill-Oriented")
        console.print("\t5. Others")

        inp = console.input("[black] [Enter your choice]: ")
        while (inp not in "12345"):
            print("\033[1A\033[2K", end='')
            inp = console.input("[black]Enter your choice: ")
        
        goal_type = int(inp)
        print("\033[7A\033[0J", end='')
        console.print("Enter the number, which most suitably describes your [u]Goal Tier[/u]:-")
        console.print("\t1. Tier I (easy task / can be completed in less time)")
        console.print("\t2. Tier II")
        console.print("\t3. Tier III (hard task / big goal / would take longer periods of time)")

        inp = console.input("[black]Enter your choice: ")
        while inp not in "123":
            print("\033[1A\033[2K", end='')
            inp = console.input("[black]Enter your choice: ")
        
        tier = int(inp)

        print("\033[7A\033[0J", end='')
        console.print("Now, write about the [i]details[/i] of the goal. Try to accomodate [u]one detail per line[/u].")
        console.print("[black](when finished, press [b]'Enter'[/b] twice; \"\" indicates the end of goal details.)", end="\n\n")
        console.print("[red][+][red][black] At least [u]one line containing at least 5 words[/u] describing your goal is required.")
        details = []
        while details == [] and len((inp := input()).split()) < 5:
            print("\033[1A\033[2K", end='')
        details.append(inp)
        while (inp := input()) != "":
            details.append(inp)
        
        print(f"\033[{len(details)+5}A\033[0J", end="")
        console.print("[blue][+][/blue] Processing Data...")
        
        dt = str(datetime.datetime.now())
        goal_record = (Application.GOAL_TYPES[goal_type-1], tier, '\n'.join(details), 'In Progress', dt, 'NULL', )
        db.insert_goal_record(goal_record)
        console.print(f"[green][+][/green] Goal record saved to database successfully with Start Time [green]=>[/green] {dt}")
        console.input("[black]Press [b]'Enter'[/b] to return to Home Menu ")

    @staticmethod
    def view_profile():
        console.print("[bold blue underline]Profile", end="\n\n")

        name = ' '.join(db.getUserName())
        exp  = db.getExperiencePts()

        console.print(f"[black]Name:[/black]\t\t[cyan italic underline]{name}")
        console.print(f"{Application.getRank(exp)}")
        console.print(f"[black]Exp. Pts.:[/black]\t[i]{exp}")
        console.input()

    @staticmethod
    def home_screen() -> None:
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
            Application.new_goal()
        elif inp.lower() == 'p':    # go to profile
            Application.view_profile()
        
    @staticmethod
    def new_comer_screen() -> None:
        console.print("[bold italic blue]   Welcome to")
        console.print("[bold blue underline]GAMIFY LIFE[/bold blue underline] [italic]~ GLi ~[/italic]", end="\n\n")

        console.input("Ready to lead a [blue underline]life[/blue underline] full of [i]ambitions[/i] and [i]goals[/i]? ")
        print("\033[1A\033[2K", end = '')

        console.print("Alright! Let's get Started...")
        fname = Application.process_name()

        print("\033[2A\033[0J", end = '')
        console.input(f"Awesome [blue]{fname}[/blue]!\nPress [b]Enter[/b] to reach [u]Home Menu[/u]. ")

    @staticmethod
    def process_name() -> str:
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