import logging as lg
from pathlib import Path

logFile = Path(__file__).resolve().parent / "data.log"

lg.basicConfig(
    level=lg.DEBUG,
    filename=logFile,
    format="%(levelname)s: %(message)s (%(asctime)s)",
)


def logInfo(msg):
    print(msg)
    lg.info(msg=msg)
