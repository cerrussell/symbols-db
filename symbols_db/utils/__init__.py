from pathlib import Path
import os
from symbols_db import DEBUG_MODE, WRAPDB_LOCATION
from symbols_db import BOM_LOCATION

HOME_DIRECTORY = Path.home()

def _create_python_dirs():
    wl = Path(WRAPDB_LOCATION)
    bl = Path(BOM_LOCATION)
    os.makedirs(wl, exist_ok=True)
    os.makedirs(bl, exist_ok=True)

    if DEBUG_MODE:
        print(f"{wl} created")
        print(f"{bl} created")

_create_python_dirs()