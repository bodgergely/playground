import logging
import random

logger = logging.getLogger('fileLogger')
fh = logging.FileHandler('logs/pythonlogging.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


def generate_message(msg_len):
    msg = ""
    for i in range(msg_len):
        c = random.randint(ord('a'), ord('z'))
        msg += chr(c)
    return msg

def run(log_count, msg_len):
    msg = generate_message(msg_len)
    for i in range(log_count):
        logger.info(msg)


log_count = 100000
msg_len = 1000
run(log_count, msg_len)
