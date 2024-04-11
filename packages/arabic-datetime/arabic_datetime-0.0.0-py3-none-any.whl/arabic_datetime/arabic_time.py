from typing import Union
import datetime

# Import constants
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

    def time(self, separator: str = ":") -> str:
        if not isinstance(separator, str):
            raise TypeError(
                f"Arabic_Date class error: The 'separator' parameter passed to the class method '{self.time.__name__}' is not a string.")
        return self.__hour.translate(self.num_trans_table) + separator + self.__minute.translate(self.num_trans_table) + separator + self.__second.translate(self.num_trans_table)
