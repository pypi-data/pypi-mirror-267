from typing import Union
import datetime

# Import constants
from . constants import MONTH_GROUPS, AR_NUMS


class Arabic_Date:
    def __init__(self, date_object: Union[datetime.date, datetime.datetime]) -> None:
        if not isinstance(date_object, datetime.date) and not isinstance(date_object, datetime.datetime):
            raise TypeError(
                "Arabic_Date class error: The parameter provided to the instance is not a datetime.date object nor a datetime.datetime object.")

        self.date_object = date_object

        self.__year = str(self.date_object.year)
        self.__month = int(self.date_object.month)
        # convert first to `int` to turn 01 into 1
        self.__day = str(int(self.date_object.day))

        # string keys in translate table must be of length 1
        self.num_trans_table = str.maketrans(AR_NUMS)

    def syriac_names(self) -> str:
        return self.__day.translate(self.num_trans_table) + " " + MONTH_GROUPS["syriac"]["months"][self.__month-1] + " " + self.__year.translate(self.num_trans_table)

    def roman1_names(self) -> str:
        return self.__day.translate(self.num_trans_table) + " " + MONTH_GROUPS["roman1"]["months"][self.__month-1] + " " + self.__year.translate(self.num_trans_table)

    def french_names(self) -> str:
        return self.__day + " " + MONTH_GROUPS["french"]["months"][self.__month-1] + " " + self.__year

    def roman2_names(self) -> str:
        return self.__day + " " + MONTH_GROUPS["roman2"]["months"][self.__month-1] + " " + self.__year

    def dual_names(self, first: str, second: str, eastern_nums: bool = False) -> str:
        if not isinstance(first, str):
            raise TypeError(
                f"Arabic_Date class error: Unknown month group name: '{first}' passed as a parameter to the method '{self.dual_names.__name__}'.")
        elif not isinstance(second, str):
            raise TypeError(
                f"Arabic_Date class error: Unknown month group name: '{second}' passed as a parameter to the method '{self.dual_names.__name__}'.")
        elif not isinstance(eastern_nums, bool):
            raise TypeError(
                f"Arabic_Date class error: eastern_nums must be a boolean. '{eastern_nums}' is not boolean and was passed to the method '{self.dual_names.__name__}'.")

        if first.strip().lower() == second.strip().lower():
            raise ValueError(
                f"Arabic_Date class error: The first group name and the second group name sould not be identicial: '{first}' was passed as the first and the second parameter to the method {self.dual_names.__name__}. Note that these particular parameters are not case sensitive.")
        valid_first_group = False
        valid_second_group = False
        for group, _ in MONTH_GROUPS.items():
            if first.lower() in group:
                valid_first_group = True
        for group, _ in MONTH_GROUPS.items():
            if second.lower() in group:
                valid_second_group = True
        if not valid_first_group or not valid_second_group:
            error_submessage = ""
            if not valid_first_group:
                error_submessage += f"Unknown first groupe name  '{
                    first}'"
            if not valid_second_group:
                if error_submessage == "":
                    error_submessage += f"Unknown second groupe name '{
                        second}'"
                else:
                    error_submessage += f" and also unknown second groupe name '{
                        second}'"
            raise ValueError(
                f"Arabic_Date class error: {error_submessage} in the parameters passed to the method '{self.dual_names.__name__}'.")

        if eastern_nums == True:
            return self.__day.translate(self.num_trans_table) + " " + MONTH_GROUPS[first]["months"][self.__month-1] + " (" + MONTH_GROUPS[second]["months"][self.__month-1] + ") " + self.__year.translate(self.num_trans_table)
        else:
            return self.__day + " " + MONTH_GROUPS[first]["months"][self.__month-1] + " (" + MONTH_GROUPS[second]["months"][self.__month-1] + ") " + self.__year

    def eastern_numeric_date(self, separator: str = "/") -> str:
        if not isinstance(separator, str):
            raise TypeError(
                f"Arabic_Date class error: 'separator' parameter must be a string. Non string value was passed to the method '{self.eastern_numeric_date.__name__}'.")
        return self.__day.translate(self.num_trans_table) + separator + str(self.__month).translate(self.num_trans_table) + separator + self.__year.translate(self.num_trans_table)

    def by_country_code(self, country_code: str) -> str:
        if not isinstance(country_code, str):
            raise TypeError(
                "Arabic_Date class error: The second provided parameter is not a string.")
        for _, group in MONTH_GROUPS.items():
            if country_code.upper() in group["countries"]:
                if group["eastern_nums"]:
                    return self.__day.translate(self.num_trans_table) + " " + group["months"][self.__month-1] + " " + self.__year.translate(self.num_trans_table)
                else:
                    return self.__day + " " + group["months"][self.__month-1] + " " + self.__year
        else:
            raise ValueError(
                f"Arabic_Date class error: Unknown country code '{country_code}'.")
