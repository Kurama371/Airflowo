import logging
import sys


class PrintToLogger:
    def __init__(self, logger):
        self.logger = logger

    def write(self, message):
        if message.strip():
            self.logger.info(message.strip())

    def flush(self):
        pass

#redirects any console outputs to logging system instead so stuff ran in asyncio's diff threads for example also get logged
def setupLogging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    sys.stdout = PrintToLogger(logging.getLogger("stdout"))
    sys.stderr = PrintToLogger(logging.getLogger("stderr"))