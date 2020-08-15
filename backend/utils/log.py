import os
import logging


class Logger:
    logger = None

    def my_logger(self):
        if self.logger is None:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            base_path = os.path.dirname(__file__)
            log_path = os.path.join(base_path, '../err.log')
            handler = logging.FileHandler(log_path)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self.logger


logger = Logger()
custom_logger = logger.my_logger()
