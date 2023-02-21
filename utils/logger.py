import utils.constants as constants

def log_message(message):
    with open(constants.LOG_PATH, 'a') as f: f.write(message + "\n")