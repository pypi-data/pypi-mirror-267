from datetime import datetime, timedelta

import numpy as np


def fill_missing_dates(data: np.ndarray, date_column_idx: int, datetime_format: str) -> np.ndarray:
    """
    Fill missing dates with forward filling
    :param data: data set with missing dates
    :param date_column_idx: index of the date column
    :param datetime_format: datetime format (e.g.%Y-%m-%d %H:%M:%S)
    :return: filled data set
    """
    end: int = len(data)
    result: list = []
    date_column: np.ndarray = data[:, date_column_idx]
    date_column = [datetime.strptime(str(i), datetime_format) for i in date_column]

    def fill_gap(i: int):
        result.append(data[i])
        i_date: datetime = date_column[i]
        while True:
            next_date: datetime = i_date + timedelta(days=1)
            if date_column[i + 1] == next_date:
                break
            next_row: list = list(data[i])
            next_row[date_column_idx] = next_date.strftime(datetime_format)
            result.append(next_row)
            i_date = next_date

    [fill_gap(i) for i in range(end - 1)]
    return np.array(result)
