import logging

def read_from_file(file_path, mode):
    try:
        with open(file_path, mode) as fd:
            return fd.read()
    except IOError as e:
        logging.info(e)
        return None
