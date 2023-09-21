import colorlog
import logging
#%(message)s ->%(pathname)s:%(lineno)d 
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

logging.basicConfig(
    level=logging.INFO,  # Set the desired log level (e.g., INFO, DEBUG, ERROR)
    handlers=[
        logging.FileHandler('coreApp.log'),  # Log to a file
        handler  # Log to the console
    ]
)