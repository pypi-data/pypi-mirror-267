"""logger module for moop."""

import sys

from loguru import logger

# logger.level('TRADER', no=29, color='<green>', icon='[@]')
# logger.level('VERBOSE', no=6, color='<yellow>', icon='[@]')

# LOGGER_FORMAT = '<green>{time:YYYY-MM-DD HH:mm:ss}</green> [ <level>{level: <8}</level> ] <level>{message}</level>'
LOGGER_FORMAT = '[ <level>{level: <8}</level> ] <level>{message}</level>'


def reset(verbose=None, **kwargs):
    logger.remove()

    levels = ['WARNING', 'INFO', 'DEBUG', 'TRACE']
    levels = (levels[verbose], levels[-1])[verbose > len(levels)]

    if kwargs.get('quiet'):
        logger.remove()
    else:
        logger.add(sys.stdout, level=levels, format=LOGGER_FORMAT)
        # logger.add(sys.stdout, level=levels)

    logger.add('runtime/_logs/trace-{time}.log', format='{time:YYYY-MM-DD HH:mm:ss} {level} {message}', level='TRACE',
               filter='whisper')
    logger.add('runtime/_logs/debug-{time}.log', format='{time:YYYY-MM-DD HH:mm:ss} {level} {message}', level='DEBUG',
               filter='whisper')

    return logger


__all__ = ('logger',)
