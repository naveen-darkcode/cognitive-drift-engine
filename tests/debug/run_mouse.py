from database.db import create_table
from collector.mouse_listener import start_mouse_listener

create_table()

start_mouse_listener()