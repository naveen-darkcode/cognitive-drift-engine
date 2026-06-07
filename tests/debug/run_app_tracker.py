from database.db import create_table
from collector.app_switch_tracker import start_app_switch_tracker

create_table()

start_app_switch_tracker()