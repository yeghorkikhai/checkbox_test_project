import os
from loguru import logger

logger.add(
    os.path.abspath('logs/log.json'),
    format='{time} {level} {message}',
    rotation='1 MB',
    compression='zip',
    colorize=True,
    serialize=True
)
