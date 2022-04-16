# coding: utf-8
from datetime import datetime as dt

COLOR_NAME_MAPPING = {
    "#000000": "Black",
    "#00756F": "Dark Teal",
    "#009EAA": "Teal",
    "#00A368": "DarkGreen",
    "#00CC78": "Green",
    "#00CCC0": "LightTeal",
    "#2450A4": "DarkBlue",
    "#3690EA": "Blue",
    "#493AC1": "Indigo",
    "#515252": "DarkGray",
    "#51E9F4": "LightBlue",
    "#6A5CFF": "Periwinkle",
    "#6D001A": "Burgundy",
    "#6D482F": "DarkBrown",
    "#7EED56": "LightGreen",
    "#811E9F": "DarkPurple",
    "#898D90": "Gray",
    "#94B3FF": "Lavender",
    "#9C6926": "Brown",
    "#B44AC0": "Purple",
    "#BE0039": "DarkRed",
    "#D4D7D9": "LightGray",
    "#DE107F": "Magenta",
    "#E4ABFF": "PalePurple",
    "#FF3881": "Pink",
    "#FF4500": "Red",
    "#FF99AA": "LightPink",
    "#FFA800": "Orange",
    "#FFB470": "Beige",
    "#FFD635": "Yellow",
    "#FFF8B8": "PaleYellow",
    "#FFFFFF": "White"
}


class RPlaceRecord:
    def __init__(self):
        self.date = ""
        self.user = ""
        self.color = ""
        self.color_name = ""
        self.x = 0
        self.y = 0

    def from_csv_line_ugly(self, line: str):
        """ Useful only for inserting data with python clickhouse-driver as it needs date to be
            either a DateTime or an int
        """
        fields = line.split(',')
        date_str = fields[0][:-4]  # 2022-04-04 00:53:51.577 UTC
        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])
        hour = int(date_str[11:13])
        minute = int(date_str[14:16])
        second = int(date_str[17:19])
        milliseconds = 0
        if len(date_str) >= 20:
            milliseconds = int(date_str[20:23])
        self.date = int(dt(year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=milliseconds * 1000).timestamp() * 1000)
        self.user = fields[1]
        self.color = fields[2]
        self.color_name = COLOR_NAME_MAPPING[self.color]
        self.x = int(fields[3][1:])
        self.y = int(fields[4][:-2])

    def from_csv_line(self, line: str):
        fields = line.split(',')
        self.date = fields[0][:-4]
        self.user = fields[1]
        self.color = fields[2]
        self.color_name = COLOR_NAME_MAPPING[self.color]
        self.x = int(fields[3][1:])
        self.y = int(fields[4][:-2])

    def to_tuple(self):
        return self.date, self.user, self.color, self.color_name, self.x, self.y

    def to_csv_line(self):
        return f"{self.date},{self.user},{self.color},{self.color_name},{self.x},{self.y}\n"

    def __str__(self):
        return f"RPlaceRecord : {str(self.date)} | {self.user} | {self.color} | {self.color_name} | {self.x} | {self.y}"
