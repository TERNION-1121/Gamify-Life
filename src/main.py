from utils.utils import Application
from utils.dbconfig import db
import os

os.system("cls")
if db.is_empty():
    Application.new_comer_screen()
    os.system("cls")

while Application.running:
    os.system("cls")
    Application.home_screen()