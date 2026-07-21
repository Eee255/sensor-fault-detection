"""
logging is — Python's built-in notebook. Instead of using print(), professional programs use logging because it can:

add a timestamp automatically
label messages as INFO, WARNING, ERROR, etc.
be turned on/off or saved to a file easily
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

list_of_files = [
    "src/sensor_fault_detection/components/__init__.py",
    "src/sensor_fault_detection/pipeline/__init__.py",
    "src/sensor_fault_detection/entity/__init__.py",
    "src/sensor_fault_detection/config/__init__.py",
    "src/sensor_fault_detection/utils/__init__.py",
    "src/sensor_fault_detection/logger/__init__.py",
    "src/sensor_fault_detection/exception/__init__.py",
    "src/sensor_fault_detection/constants/__init__.py",
    "tests/__init__.py",
    ".github/workflows/ci.yaml",
]


for filepath_str in list_of_files:
    filepath = Path(filepath_str)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    if not filepath.exists():
        filepath.touch()
        logging.info(f"created: {filepath}")
    elif filepath.stat().st_size == 0:
        logging.info(f"exists (empty, owned by template): {filepath}")
    else:
        logging.info(f"skipped (has content): {filepath}")