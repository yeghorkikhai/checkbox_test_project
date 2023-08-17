import os
from loguru import logger

logger.add(
    os.path.abspath('logs/log.log'),
    format='{time} {level} {message}',
    rotation='1 MB',
    compression='zip',
    colorize=True,
    # serialize=True
    # if True logs will write to json
)
