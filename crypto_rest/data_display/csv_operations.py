import csv
import os


class CsvWritter:

    def __init__(self, path):
        self._path = path


    def write_result_into_file(self, result_loader):
        if not os.path.exists(self._path):
            mode = 'xt'
        else:
            mode = 'a'
        with open(self._path, mode) as f:
            f_csv = csv.writer(f)
            f_csv.writerow(result_loader.csv_headers())
            for r in result_loader:
                f_csv.writerow(r)