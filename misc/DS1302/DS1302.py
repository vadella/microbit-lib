"""
    Adapted from 
    https://github.com/shaoziyang/microbit-lib/tree/master/misc/DS1302
    
    Changes:
    --------
    - Working with @property
    - Adapted fo Circuitpython

    
    DS1302 RTC drive

    Author: shaoziyang
    Date:   2018.3

    http://www.micropython.org.cn
"""

from digitalio import Direction

DS1302_REG_SECOND = 0x80
DS1302_REG_MINUTE = 0x82
DS1302_REG_HOUR = 0x84
DS1302_REG_DAY = 0x86
DS1302_REG_MONTH = 0x88
DS1302_REG_WEEKDAY = 0x8A
DS1302_REG_YEAR = 0x8C
DS1302_REG_WP = 0x8E
DS1302_REG_CTRL = 0x90
DS1302_REG_RAM = 0xC0


def DecToHex(dat):
    return (dat // 10) * 16 + (dat % 10)


def HexToDec(dat):
    return (dat // 16) * 10 + (dat % 16)


class DS1302:
    def __init__(self, clk, dio, cs):
        self.clk = clk
        self.dio = dio
        self.cs = cs
        self.clk.direction = Direction.OUTPUT
        self.cs.direction = Direction.OUTPUT

        self.cs.value = False
        self.clk.value = False

    def write_byte(self, dat):
        self.dio.direction = Direction.OUTPUT
        for i in range(8):
            self.dio.value = (dat >> i) & 1
            self.clk.value = True
            self.clk.value = False

    def read_byte(self):
        d = 0
        self.dio.direction = Direction.INPUT
        for i in range(8):
            d = d | (self.dio.value << i)
            self.clk.value = True
            self.clk.value = False
        return d

    def getReg(self, reg):
        self.cs.value = True
        self.write_byte(reg)
        t = self.read_byte()
        self.cs.value = False
        return t

    def setReg(self, reg, dat):
        self.cs.value = True
        self.write_byte(reg)
        self.write_byte(dat)
        self.cs.value = False

    def wr(self, reg, dat):
        self.setReg(DS1302_REG_WP, 0)
        self.setReg(reg, dat)
        self.setReg(DS1302_REG_WP, 0x80)

    def start(self):
        t = self.getReg(DS1302_REG_SECOND + 1)
        self.wr(DS1302_REG_SECOND, t & 0x7F)

    def stop(self):
        t = self.getReg(DS1302_REG_SECOND + 1)
        self.wr(DS1302_REG_SECOND, t | 0x80)

    @property
    def second(self):
        return HexToDec(self.getReg(DS1302_REG_SECOND + 1)) % 60

    @second.setter
    def second(self, second):
        print("setting second: ", second)
        self.wr(DS1302_REG_SECOND, DecToHex(second % 60))

    @property
    def minute(self):
        return HexToDec(self.getReg(DS1302_REG_MINUTE + 1))

    @minute.setter
    def minute(self, minute):
        print("setting minute: ", minute)
        self.wr(DS1302_REG_MINUTE, DecToHex(minute % 60))

    @property
    def hour(self):
        return HexToDec(self.getReg(DS1302_REG_HOUR + 1))

    @hour.setter
    def hour(self, hour):
        print("setting hour: ", hour)
        self.wr(DS1302_REG_HOUR, DecToHex(hour % 24))

    @property
    def weekday(self):
        return HexToDec(self.getReg(DS1302_REG_WEEKDAY + 1))

    @weekday.setter
    def weekday(self, weekday):
        print("setting weekday: ", weekday)
        self.wr(DS1302_REG_WEEKDAY, DecToHex(weekday % 7))

    @property
    def day(self):
        return HexToDec(self.getReg(DS1302_REG_DAY + 1))

    @day.setter
    def day(self, day):
        print("setting day: ", day)
        self.wr(DS1302_REG_DAY, DecToHex(day % 32))

    @property
    def month(self):
        return HexToDec(self.getReg(DS1302_REG_MONTH + 1))

    @month.setter
    def month(self, month):
        print("setting month: ", month)
        self.wr(DS1302_REG_MONTH, DecToHex(month % 13))

    @property
    def year(self):
        return HexToDec(self.getReg(DS1302_REG_YEAR + 1)) + 2000

    @year.setter
    def year(self, year):
        print("setting year: ", year)
        self.wr(DS1302_REG_YEAR, DecToHex(year % 100))

    @property
    def datetime(self):
        return (
            self.year,
            self.month,
            self.day,
            self.weekday,
            self.hour,
            self.minute,
            self.second,
        )

    @datetime.setter
    def datetime(self, dat):
        print("setting", dat)
        (
            self.year,
            self.month,
            self.day,
            self.weekday,
            self.hour,
            self.minute,
            self.second,
        ) = dat

    def ram(self, reg, dat=None):
        if dat == None:
            return self.getReg(DS1302_REG_RAM + 1 + (reg % 31) * 2)
        else:
            self.wr(DS1302_REG_RAM + (reg % 31) * 2, dat)

