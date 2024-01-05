import logging
class Logger:
    def __init__(self):
        pass
    def createLog_data(self,data, log_file='my_log.log'):
        try:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s]: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=log_file,
                filemode='a'
            )
            logging.log(logging.INFO,data)
            return True
        except Exception as e:
            print(f"error in createLog:- {e}")
            return False
