from utils.dbconfig import db 

import datetime
import os

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
        console.print(f"|{'Goal Title'.center(40)}", end="")
        console.print(f"|{'Goal Status'.center(13)}", end="")
        console.print(f"|{'Start Time'.center(21)}|", end="")
        if not negate_endtime:
            width += 22
            console.print(f"{'End Time'.center(21)}|", end="")
        print("\n" + "-"*width)
        for details in records:
            goal_id, goal_type, tier, desc, status, st, et, title = details
            console.print(f"|{str(goal_id).center(9)}", end="")
            console.print(f"|{goal_type.center(21)}", end="")
            console.print(f"|{tier.center(6)}", end="")
            title = title if len(title) < 40 else title[:35] + '...'
            console.print(f"|{(title).center(40)}", end="")
            console.print(f"|{status.center(13)}", end="")
            console.print(f"|{st.center(21)}|", end="")
            if not negate_endtime:
                console.print(f"{et.center(21)}|", end="")
            print()
        print("-"*width)

class Application():
    GOAL_TYPES = ["Academic", "Sports", "Self-Oriented", "Work/Skill-Oriented", "Others"]

    RANKS      = {  1: ('Neophyte', (0, 100)), 2: ('Intermediate', (100, 300)), 
                    3: ('Adept', (300, 650)), 4: ('Prime', (650, 1000)), 
                    5: ('Paramount', (1000, 2**31-1))}
    running = True

    @staticmethod
    def check_level_update(exp: int) -> tuple:
        for rank in Application.RANKS:
            upperLimit = Application.RANKS[rank][1][1]
            if exp >= upperLimit:
                return (True, rank+1)
        return (False, None)

    @staticmethod
    def getRank(exp: int) -> str:
        for rank in Application.RANKS:
            lowerLimit, upperLimit = Application.RANKS[rank][1]
            if lowerLimit <= exp < upperLimit:
                return f"[black]Level ({rank}): [/black]\t[cyan italic underline]{Application.RANKS[rank][0]}"
    
    @staticmethod
    def view_goal_desc() -> None:
        goals = db.get_all_goals()
        valid_ids = [i[0] for i in goals]
        goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to be viewed: ")
        while int(goal_id) not in valid_ids:
            print("\033[1A\033[0J", end='')
            goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to be viewed [Invalid Goal ID was entered]: ")
        print("\033[1A\033[0J", end='')

        record = db.get_goal_details(goal_id)
        goal_type, tier, desc, status, st, et, title = record
        
        console.print(f"[blue italic underline]{title}[/blue italic underline] [italic][{goal_id}][/italic]", end='\n\n')
        console.print(f"[blue]{goal_type}[/blue] | [blue]Tier[/blue] {tier}", end='\n\n')
        console.print(f"[green][+] Started at[/green]: {st}")
        if status == "In Progress":
            color = "yellow"
        else:
            console.print(f"[blue][+] Completed at[/blue]: {et}")
            color = "green"
        console.print(f"[blue]Status[/blue]: [{color}]{status}", end='\n\n')
        console.print(f"[blue underline]Description[/blue underline]")
        console.print(f"{desc}", end='\n\n')
        
        console.input("[black]Press [b]'Enter'[/b] to return to Home Menu ")

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
        console.print("Now, type the [i]title[/i] of your goal.")
        console.print("[red][+][red][black] It is [italic]strictly recommended[/italic] to have less than 40 characters in your title.")
        console.print("[black italic]    Crisp titles are nice :]", end='\n\n')
        title = console.input()
        print("\033[1A\033[2K", end='')
        console.print(f"[yellow bold]{title}", end="\n\n")
        console.print("Now, write about the [i]details[/i] of the goal. Try to accomodate [u]one detail per line[/u].")
        console.print("[black](when finished, press [b]'Enter'[/b] twice; \"\" indicates the end of goal details.)", end="\n\n")
        console.print("[red][+][red][black] At least [u]one line containing at least 5 words[/u] describing your goal is required.")
        details = []
        while details == [] and len((inp := input()).split()) < 5:
            print("\033[1A\033[2K", end='')
        details.append(inp)
        while (inp := input()) != "":
            details.append(inp)
        
        print(f"\033[{len(details)+11}A\033[0J", end="")
        console.print("[blue][+][/blue] Processing Data...")
        
        dt = str(datetime.datetime.now()).split('.')[0]
        goal_record = (Application.GOAL_TYPES[goal_type-1], tier, '\n'.join(details), 'In Progress', dt, 'NULL', title)
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
        
        console.print(f"[italic underline]Completed Goals\n", style="#90E13F")
        completed = db.get_all_goals(goal_status="Completed")
        if len(completed) == 0:
            console.print("No completed goals :[\n[i]Why not start with one?")
        else:
            Utilities.print_goals(completed)
        
        print("\n")
        console.print(f"[italic underline]Goals in Progress\n", style="#90E13F")
        in_progress = db.get_all_goals(goal_status="In Progress")
        if len(in_progress) == 0:
            console.print("No goals in progress :[\n[i]Why not start with one?")
        else:
            Utilities.print_goals(in_progress, negate_endtime=True)

        if len(completed) + len(in_progress) == 0:
            console.input("\n[black]Press [b]'Enter'[/b] to return to Home Menu")
        else:
            console.print("\n[black]Press [b]'Enter'[/b] to return to Home Menu")
            console.print("[black]Press [b]'V'[/b] then [b]'Enter'[/b] to enter View Goal Mode")
            while (inp := input()):
                match inp.lower():
                    case '':
                        break
                    case 'v':
                        print("\033[3A\033[0J", end='')
                        Application.view_goal_desc()
                        break

                print("\033[1A\033[2K", end='')

    @staticmethod
    def home_screen() -> None:
        console.print("[bold blue underline]Home", end="\n\n")
        Utilities.greet()
        console.print("\nReady to take on another challenge?")
        console.print("[black][Press 'P' then 'Enter' to view profile]")
        console.print("[black][Press 'S' then 'Enter' to begin with another goal]")
        console.print("[black][Press 'E' then 'Enter' to complete a goal in progress]")
        console.print("[black][Press 'D' then 'Enter' to dump a goal in progress]")
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
            valid_ids = [i[0] for i in in_progress_goals]
            print("\n")
            goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to set complete: ")
            while int(goal_id) not in valid_ids:
                print("\033[1A\033[0J", end='')
                goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to set complete [Invalid Goal ID was entered]: ")
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
                console.print(f"[green][+][/green] You earned {db.update_exp(goal_id)} exp. pts. completing the goal")

                t = Application.check_level_update(db.getExperiencePts())
                if t[0]:
                    console.print("[yellow][+][/yellow] Congratulations! You ranked up!")
                    console.print(f"\tYour updated rank [green]=>[/green] [cyan italic]({t[1]}): [u]{Application.RANKS[t[1]][0]}")
                

        console.input("\n[black]Press [b]'Enter'[/b] to return to Home Menu ")

    @staticmethod
    def dump_goal() -> None:
        console.print("[bold blue underline]Goals in Progress", end="\n\n")

        in_progress_goals = db.get_all_goals("In Progress")
        if in_progress_goals == []:
            console.print("Seems like there are no goals to dump!")
        else:
            Utilities.print_goals(in_progress_goals, negate_endtime=True)
            valid_ids = [i[0] for i in in_progress_goals]
            print("\n")
            goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to dump: ")
            while int(goal_id) not in valid_ids:
                print("\033[1A\033[0J", end='')
                goal_id = console.input("[black]Enter the [u]Goal ID[/u] of the goal to dump [Invalid Goal ID was entered]: ")
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