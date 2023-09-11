from utils.utils import Application
from utils.dbconfig import db
import os

os.system("clear")
if db.is_empty():
    Application.new_comer_screen()
    os.system("clear")

Application.home_screen()