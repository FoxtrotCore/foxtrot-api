import foxtrot_api
from loguru import logger
from datetime import datetime


def enable_retention(filename: str, duration: str = '10 days'):
    """
    Enables logfile retention for a specified length of time. ['10 days']
    """
    logger.add(filename, retention=duration)  # Cleanup after duration
    logger.add(filename, compression="zip")    # Compress history


def init(name, retain_log: bool = False, duration: str = '10 days'):
    """
    Initializes the server logger.

    Parameters
    ----------
    name : name of the application initiating the logger
    """
    filename = "/var/log/{}-{}-{}.log" \
               .format(foxtrot_api.APP_NAME,
                       name,
                       datetime.now().strftime("%m_%d_%y"))
    logger.add(filename,
               rotation="00:00",
               format="<green>{time}</green> <level>{message}</level>")
    logger.warning("Logs will saved at {}".format(filename))

    if(retain_log):
        enable_retention(filename, duration=duration)
