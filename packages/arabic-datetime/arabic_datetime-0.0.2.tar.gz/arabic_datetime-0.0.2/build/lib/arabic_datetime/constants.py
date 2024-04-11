# Constants
AR_NUMS = {
    "0": "٠",
    "1": "١",
    "2": "٢",
    "3": "٣",
    "4": "٤",
    "5": "٥",
    "6": "٦",
    "7": "٧",
    "8": "٨",
    "9": "٩"
}

ALL_COUNTRY_CODES = [
    "DZ",
    "BH",
    "KM",
    "DJ",
    "EG",
    "IQ",
    "JO",
    "KW",
    "LB",
    "LY",
    "MR",
    "MA",
    "OM",
    "PS",
    "QA",
    "SA",
    "SO",
    "SD",
    "SY",
    "TN",
    "AE",
    "YE"
]

MONTH_GROUPS = {
    "syriac": {
        "eastern_nums": True,
        "months": [
            "كانون الثاني",
            "شباط",
            "آذار",
            "نيسان",
            "أيار",
            "حزيران",
            "تموز",
            "آب",
            "أيلول",
            "تشرين الأول",
            "تشرين الثاني",
            "كانون الأول"
        ],
        "countries": [
            "IQ",
            "JO",
            "LB",
            "PS",
            "SO",
            "SY",
        ],
    },

    "roman1": {
        "eastern_nums": True,
        "months": [
            "يناير",
            "فبراير",
            "مارس",
            "أبريل",
            "مايو",
            "يونيو",
            "يوليو",
            "أغسطس",
            "سبتمبر",
            "أكتوبر",
            "نوفمبر",
            "ديسمبر",
        ],
        "countries": [
            "BH",
            "KM",
            "DJ",
            "EG",
            "KW",
            "LY",
            "OM",
            "QA",
            "SA",
            "SO",
            "SD",
            "AE",
            "YE",
        ],
    },
    "roman2": {
        "eastern_nums": False,
        "months": [
            "يناير",
            "فبراير",
            "مارس",
            "أبريل",
            "ماي",
            "يونيو",
            "يوليوز",
            "غشت",
            "شتنبر",
            "أكتوبر",
            "نونبر",
            "دجنبر",
        ],
        "countries": [
            "MA",
            "MR",
        ]
    },

    "french": {
        "eastern_nums": False,
        "months": [
            "جانفي",
            "فيفري",
            "مارس",
            "أفريل",
            "ماي",
            "جوان",
            "جويلية",
            "أوت",
            "سبتمبر",
            "أكتوبر",
            "نوفمبر",
            "ديسمبر",
        ],
        "countries": [
            "DZ",
            "TN",
        ]
    },
}


COUNTRY_CODES_DICT = {
    "DZ": "Algeria",
    "BH": "Bahrain",
    "KM": "Comoros",
    "DJ": "Djibouti",
    "EG": "Egypt",
    "IQ": "Iraq",
    "JO": "Jordan",
    "KW": "Kuwait",
    "LB": "Lebanon",
    "LY": "Libya",
    "MR": "Mauritania",
    "MA": "Morocco",
    "OM": "Oman",
    "PS": "Palestine",
    "QA": "Qatar",
    "SA": "Saudi Arabia",
    "SO": "Somalia",
    "SD": "Sudan",
    "SY": "Syria",
    "TN": "Tunisia",
    "AE": "United Arab Emirates",
    "YE": "Yemen"
}

DUAL_MONTHS = {
    "1": "كانون الثاني (يناير)",
    "2": "شباط (فبراير)",
    "3": "آذار (مارس)",
    "4": "نيسان (أبريل)",
    "5": "أيار (مايو)",
    "6": "حزيران (يونيو)",
    "7": "تموز (يوليو)",
    "8": "آب (أغسطس)",
    "9": "أيلول (سبتمبر)",
    "10": "تشرين الأول (أكتوبر)",
    "11": "تشرين الثاني (نوفمبر)",
    "12": "كانون الأول (ديسمبر)"
}
