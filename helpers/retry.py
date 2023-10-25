import time

MAX_RETRIES = 5


def retry(func):
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                time.sleep(10)
                retries += 1

    return wrapper
