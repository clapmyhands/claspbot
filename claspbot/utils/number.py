import logging

logger = logging.getLogger('discord')


def parse_int(msg):
    try:
        return int(msg)
    except ValueError as ve:
        logger.error(ve)
        return None
