from datetime import datetime


def convert_unix_to_date(unix_time: int):
    return datetime.fromtimestamp(unix_time).strftime('%d/%m/%Y')

