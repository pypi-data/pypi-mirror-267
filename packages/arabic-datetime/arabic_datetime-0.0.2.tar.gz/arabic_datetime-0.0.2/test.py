# from arabic_datetime import Arabic_Date, Arabic_Time
from arabic_datetime import Arabic_Date
from arabic_datetime import Arabic_Time
import datetime


if __name__ == "__main__":
    arabic_date = Arabic_Date(datetime.date.today())
    arabic_date = Arabic_Date(datetime.datetime(
        1980, 8, 16, 12, 30, 45, 100000))
    arabic_time = Arabic_Time(datetime.datetime(
        1980, 8, 16, 12, 30, 45, 100000))
    arabic_time = Arabic_Time(datetime.time(12, 30, 45, 100000))
    arabic_time = Arabic_Time(datetime.time(12, 30, 45))
    arabic_time = Arabic_Time(datetime.time(12, 30))

    # print(arabic_date.syriac_names(True))
    # print(arabic_date.roman1_names(True))
    # print(arabic_date.french_names(True))
    # print(arabic_date.roman2_names(True))

    # print("+++++++++++++++++++++++++++++++")

    # print(arabic_date.by_country_code("SY", True))
    # print(arabic_date.by_country_code("DZ"))
    # print(arabic_date.by_country_code("EG", True))
    # print(arabic_date.by_country_code("MA"))

    # print(arabic_date.by_country_code(True))

    # print("+++++++++++++++++++++++++++++++")

    print(arabic_time.time())
    print(arabic_time.time("5", "HMS"))

    # print("+++++++++++++++++++++++++++++++")

    # print(arabic_date.dual_names(first="syriac",
    #       second="roman1", east_nums=True))
    # print(arabic_date.dual_names(first="syriac",
    #       second="french", eastern_nums=False))
    # print(arabic_date.dual_names(first="syriac",
    #       second="morocco", eastern_nums=False))

    # print("+++++++++++++++++++++++++++++++")

    # print(arabic_date.eastern_numeric_date("/"))

    # dual_date_ro_sy = arabic_date.dual_names("roman1", "syriac", True)
    # print(dual_date_ro_sy)
