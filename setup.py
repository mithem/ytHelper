import os
import utils
from utils import col
from pathlib import Path


try:
    utils.setUpDirs()

    if not os.path.exists("config.json"):
        f = open("config.json", "w+")
        f.close()

    utils.setUpConfig()

    print(col.OKGREEN + "Setup complete" + col.ENDC)
except Exception as e:
    print(col.FAIL + "Error: " + str(e) + col.ENDC)
