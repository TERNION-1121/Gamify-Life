from utils.utils import Application, cmd
import os

os.system(cmd)
if Application.is_database_empty():
    Application.new_comer_screen()

while Application.RUNNING:
    os.system(cmd)
    Application.home_screen()