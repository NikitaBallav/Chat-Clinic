import os
from pathlib import Path
import logging

# os: Provides functions to interact with the operating system, such as file and directory management.
# Path from pathlib: A more modern way to handle filesystem paths (compared to os.path).
# logging: A built-in Python module for logging messages (info, warnings, errors, etc.).


logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# level=logging.INFO → Sets the logging level to INFO, so only INFO and higher-level messages will be logged.
# format='[%(asctime)s]: %(message)s:' → Defines the log message format:
# %(asctime)s → Adds a timestamp.
# %(message)s → Displays the actual log message.

# In Python's logging module, log messages have different severity levels, ordered from lowest to highest:
# (DIWEC)

# DEBUG (10) - Detailed debugging messages.
# INFO (20) - General information about the program's execution.
# WARNING (30) - Indicates something unexpected but not critical.
# ERROR (40) - A serious issue that prevents part of the program from running.
# CRITICAL (50) - A very serious issue that may crash the application.

# What does level=logging.INFO mean?

# It filters out lower-level messages (DEBUG).
# It logs only messages with level INFO and above (INFO, WARNING, ERROR, CRITICAL).


list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]


for filepath in list_of_files:
    filepath= Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")
    
    # exist_ok=True ensures that if the directory already exists, it does not recreate it.
    # It will only create missing directories.


    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    # If the file already exists and is not empty, it does nothing.
    # If the file does not exist, or is empty, it creates an empty file.
    # If the file is empty (os.path.getsize(filepath) == 0 returns True), the code inside the if block runs. The script opens the file in "w" mode, which technically recreates it as an empty file.
    
    else:
        logging.info(f"{filename} already exists")


