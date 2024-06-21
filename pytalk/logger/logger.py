import json 
import logging 
import logging.config
import os
import sys

def get_logger(name=os.path.basename(sys.path[0])) -> logging.Logger:

    with open("pytalk/logger/config.json", "r") as fin: 
        config = json.load(fin)
    logging.config.dictConfig(config=config)

    return logging.getLogger(name=name)

if __name__ == "__main__":
    logger = get_logger()
    logger.info("Why is the timezone string so damn long??")