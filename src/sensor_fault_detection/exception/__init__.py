import sys


def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return (
        f"Error occurred in script [{file_name}] "
        f"at line [{line_number}]: {str(error)}"
    )


class SensorException(Exception):
    def __init__(self, error, error_detail):
        self.error_message = error_message_detail(error, error_detail)
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message