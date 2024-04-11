from typing import Union
import datetime

# Import from constants
from . constants import AR_NUMS


class Arabic_Time:
    def __init__(self, time_object: Union[datetime.time, datetime.datetime]) -> None:
        if not isinstance(time_object, datetime.time) and not isinstance(time_object, datetime.datetime):
            raise TypeError(
                f"Arabic_Time class error: The parameter passed to the instance is not a datetime.time object nor a datetime.datetime object.")

        self.time_object = time_object

        # string keys in translate table must be of length 1
        self.num_trans_table = str.maketrans(AR_NUMS)

        # convert first to `int` to turn 01 into 1
        self.__hour = str(int(self.time_object.hour))
        self.__minute = str(int(self.time_object.minute))
        self.__second = str(int(self.time_object.second))
        self.__microsecond = str(int(self.time_object.microsecond))

    def time(self, format: str = "HMS", separator: str = ":") -> str:
        if not isinstance(format, str):
            raise TypeError(
                f"Arabic_Date class error: The 'format' parameter passed to the class method '{self.time.__name__}' is not a string.")
        elif not isinstance(separator, str):
            raise TypeError(
                f"Arabic_Date class error: The 'separator' parameter passed to the class method '{self.time.__name__}' is not a string.")

        if format.upper() not in ["H", "HM", "HMS", "HMSF"]:
            raise ValueError(
                f"Arabic_Date class error: Invalid format string passed to the class method '{self.time.__name__}'. Valid values are 'HMSF', 'HMS', 'HM' and 'H'.")

        time_elements = []
        if "H" in format.upper():
            time_elements.append(self.__hour.translate(self.num_trans_table))
        if "M" in format.upper():
            time_elements.append(self.__minute.translate(self.num_trans_table))
        if "S" in format.upper():
            time_elements.append(self.__second.translate(self.num_trans_table))
        if "F" in format.upper():
            time_elements.append(
                self.__microsecond.translate(self.num_trans_table))

        formated_time = separator.join(time_elements)

        return formated_time
