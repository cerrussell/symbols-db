import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(filename="error_building.log", level=logging.ERROR)

DELIMETER_BOM = "~~"
# variables
DEBUG_MODE = True
# constants
WRAPDB_LOCATION = Path("./temp/wrapdb")
BOM_LOCATION = Path("./temp/boms")
BLINTDB_LOCATION = "blint.db"
