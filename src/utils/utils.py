from utils.dbconfig import db 

import datetime
import os

import keyboard

from rich import print as printc
from rich.console import Console 
console = Console()

class Utilities():
    @staticmethod
    def is_proper_alphabetical_string(string: str):
        alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
        return all(ch in alphabets for ch in string)

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
    
    @staticmethod
    def print_goals(records, negate_endtime=False) -> None:
        width = 117
        console.print(f"| Goal ID ", end="")
        console.print(f"|{'Goal Type'.center(21)}", end="")
        console.print(f"| Tier ", end="")
        console.print(f"|{'Goal Description'.center(40)}", end="")
        console.print(f"|{'Goal Status'.center(13)}", end="")
        console.print(f"|{'Start Time'.center(21)}|", end="")
        if not negate_endtime:
            width += 21
            console.print(f"{'End Time'.center(21)}|", end="")
        print("\n" + "-"*width)
        for details in records:
            goal_id, goal_type, tier, desc, status, st, et = details
            console.print(f"|{str(goal_id).center(9)}", end="")
            console.print(f"|{goal_type.center(21)}", end="")
            console.print(f"|{tier.center(6)}", end="")
            console.print(f"|{(desc[:35] + '...').center(40)}", end="")
            console.print(f"|{status.center(13)}", end="")
            console.print(f"|{st.center(21)}|", end="")
            if not negate_endtime:
                console.print(f"{et.center(21)}|", end="")
            print()
        print("-"*width)

class Application():
    GOAL_TYPES = ["Academic", "Sports", "Self-Oriented", "Work/Skill-Oriented", "Others"]
    running = True

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
        
        dt = str(datetime.datetime.now()).split('.')[0]
        goal_record = (Application.GOAL_TYPES[goal_type-1], tier, '\n'.join(details), 'In Progress', dt, 'NULL', )
        db.insert_goal_record(goal_record)

        console.print(f"[green][+][/green] Goal record saved to database successfully with Start Time [green]=>[/green] {dt}")
        console.input("\n[black]Press [b]'Enter'[/b] to return to Home Menu ")

    @staticmethod
    def view_profile():
        console.print("[bold blue underline]Profile", end="\n\n")

        name = ' '.join(db.getUserName())
        exp  = db.getExperiencePts()

        console.print(f"[black]Name:[/black]\t\t[cyan italic underline]{name}")
        console.print(f"{Application.getRank(exp)}")
        console.print(f"[black]Exp. Pts.:[/black]\t[i]{exp}", end="\n\n")
        console.rule(characters="=")
        print("\n")
        
        console.input()

    @staticmethod
    def home_screen() -> None:
        console.print("[bold blue underline]Home", end="\n\n")
        Utilities.greet()
        console.print("\nReady to take on another challenge?")
        console.print("[black][Press 'P' then 'Enter' to view Profile]")
        console.print("[black][Press 'S' then 'Enter' to begin with another goal]")
        console.print("[black][Press 'E' then 'Enter' to complete a goal in progress]")
        console.print("[black][Press 'D' then 'Enter to dump a goal in progress]")
        console.print("[black][Press 'Q' then 'Enter' to exit the application]")
        
        while (inp := input()):
            match (inp.lower()):
                case 'p':
                    os.system("cls")
                    Application.view_profile()
                    break
                case 's':
                    os.system("cls")
                    Application.new_goal()
                    break
                case 'e':
                    os.system("cls")
                    Application.complete_goal()
                    break 
                case 'd':
                    os.system("cls")
                    Application.dump_goal()
                    break
                case 'q':
                    os.system("cls")
                    Application.running = False
                    break

            print("\033[1A\033[2K", end='')
    
    @staticmethod
    def complete_goal():
        console.print("[bold blue underline]Goals in Progress", end="\n\n")

        in_progress_goals = db.get_all_goals("In Progress")
        if in_progress_goals == []:
            console.print("Looks like there are no goals in progress :[\n[i]Why not begin with one?")
        else:
            Utilities.print_goals(in_progress_goals, negate_endtime=True)
        
            print("\n")
            goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to set complete: ")
            print(f"\033[{len(in_progress_goals) + 6}A\033[0J", end="")
            try:
                console.print("[blue][+][/blue] Processing Data...")
                dt = str(datetime.datetime.now()).split('.')[0]
                db.set_goal_finish(goal_id, dt)
            except Exception:
                console.print("[red][-][/red] An error occurred.")
                console.print_exception(show_locals=True)
            
            else: 
                console.print(f"[green][+][/green] Goal Completion successful with End Time [green]=>[/green] {dt}")

        console.input("\n[black]Press [b]'Enter'[/b] to return to Home Menu ")

    @staticmethod
    def dump_goal() -> None:
        console.print("[bold blue underline]Goals in Progress", end="\n\n")

        in_progress_goals = db.get_all_goals("In Progress")
        if in_progress_goals == []:
            console.print("Seems like there are no goals to dump!")
        else:
            Utilities.print_goals(in_progress_goals, negate_endtime=False)

            print("\n")
            goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to dump: ")
            print(f"\033[{len(in_progress_goals) + 6}A\033[0J", end="")
            try:
                console.print("[blue][+][/blue] Processing drop request...")
                db.drop_goal_record(goal_id)
            except Exception:
                console.print("[red][-][/red] An error occurred.")
                console.print_exception(show_locals=True)
            
            else: 
                console.print(f"[green][+][/green] Goal Record {goal_id} successfully deleted from database")

        console.input("\n[black]Press [b]'Enter'[/b] to return to Home Menu ")

    @staticmethod
    def new_comer_screen() -> None:
        console.print("[bold italic blue]   Welcome to")
        console.print("[bold blue underline]GAMIFY LIFE[/bold blue underline] [italic]~ GLi ~[/italic]", end="\n\n")

        console.input("Ready to lead a [blue underline]life[/blue underline] full of [i]ambitions[/i] and [i]goals[/i]? ")
        print("\033[1A\033[2K", end = '')

        console.print("Alright! Let's get Started...")
        Application.process_name()
        name = db.getUserName()

        print("\033[2A\033[0J", end = '')
        console.input(f"Awesome [blue]{name[0]}[/blue]!\nPress [b]Enter[/b] to reach [u]Home Menu[/u]. ")

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