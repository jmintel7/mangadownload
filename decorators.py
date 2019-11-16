import time
import  logging

timer = logging.getLogger()
timer.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s :%(asctime)s : %(message)s ')
file_handler = logging.FileHandler('downloads.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

timer.addHandler(file_handler)
timer.addHandler(stream_handler)


def my_time(org_fun):

    def wrapper(*args, **kwargs):
        t1 = time.time()
        org_fun(*args, **kwargs)
        t2 = time.time()
        line = f'Chapter {args[0]} took {t2-t1} sec to complete'
        timer.info(line)

    return wrapper