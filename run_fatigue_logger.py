from database.db import create_table
from collector.fatigue_logger import start_fatigue_logger

create_table()

start_fatigue_logger()