import logging
from datetime import datetime
from pathlib import Path

'''
build a filename from the current time
strftime turns a datetime into a string using a "format code"
we use underscore instead of ":" because windows doesnt allow ":" in filenames
'''
LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# 2. make sure logs folder exsits
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 3 full path to this runs log file e.g. logs/07_19_2026_18_30_40.log

LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME

# 4. configure logging to write to that file  
logging.basicConfig(filename=str(LOG_FILE_PATH), format="%(asctime)s - %(lineno)d - %(levelname)s - %(message)s", level=logging.INFO)