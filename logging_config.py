import colorlog
import logging

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s%(reset)s'':''     %(message)s :: %(pathname)s:%(lineno)d :: %(asctime)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    style='%'
))

# Use the same formatter for both console and file logging
formatter = logging.Formatter(
    '%(levelname)s: %(message)s :: %(pathname)s:%(lineno)d :: %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('coreApp.log', mode='a'),  # 'a' for append mode
        handler,
    ]
)

# Set the formatter for the file handler
logging.getLogger().handlers[0].setFormatter(formatter)
