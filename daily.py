#!/usr/bin/env python3
"""
Daily
=====

Mijery ny Teny vakina epub dia mampiseho ny andininteny androany.
"""

from bs4 import BeautifulSoup
from peewee import SqliteDatabase, Model, IntegerField, CharField

from zipfile import ZipFile
from datetime import date
from textwrap import wrap
from pathlib import Path
import calendar
import sys

today = date.today()


DAILY_FILENAME = f"es{str(today.year)[2:4]}_MG.epub"

# Apetrao ao amin'ny ~/JW/Document/epub ny boky epub"es20_MG.epub" sy "es21_MG.epub"
# na afaka solinao eo amin'ny ilay oe <PATH> ny tokony hisy azy

# Download link:
# https://download-a.akamaihd.net/files/media_publication/11/es20_MG.epub
# https://download-a.akamaihd.net/files/media_publication/04/es21_MG.epub

PATH = Path.home() / "JW/Document/epub" / DAILY_FILENAME


DAILY_FILE = ZipFile(PATH)

# Soloy teny hafa ireto raha epub amin'ny teny hafa no ampiasainao

MONTH_SHORT2LONG = [
    'janoary',
    'febroary',
    'martsa',
    'aprily',
    'mey',
    'jona',
    'jolay',
    'aogositra',
    'septambra',
    'oktobra',
    'novambra',
    'desambra', ]


def parse(file):
    """
    Mijery ny fichier anaty epub (zip)
    """

    with DAILY_FILE.open(f"OEBPS/{file}") as fp:
        parsed = BeautifulSoup(fp.read(), "html.parser")

    return parsed


def get_month_file(month=today.month, day=today.day):
    """
    Maka ny fichier misy ny andininteny androany.
    """

    month = MONTH_SHORT2LONG[month - 1].title()

    for element in parse("toc.xhtml").find_all("a"):
        if element.text == month:
            begin = element["href"]
            break

    if day == 1:
        return begin
    else:
        part = begin.split(".")
        part[0] += f"-split{day}"

        return ".".join(part)


def get_month_days(month):
    c = calendar.Calendar()
    c = list(c.itermonthdays(2021, month))
    c = list(filter(lambda x: x!=0, c))
    return list(c)[-1]


def subiter(element):
    pass


def get_text(month=today.month, day=today.day):
    """
    Maka ny soratra misy ny andininteny androany.
    """

    i = 0
    text_list = list()
    theme = parse(get_month_file(month, day)).find(attrs={"class": "themeScrp"})

    result = theme.text

    # USE bs4

    if "—" in result:
        result_text = result.split("—")[0]
        result_chap = result.split("—")[1]
    else:
        print()
        print(result)

    return [result_text, result_chap]


def main():
    db = SqliteDatabase('daily.sqlite')

    class Daily_2021(Model):
        month = IntegerField()
        day = IntegerField()

        text = CharField(max_length=1000)
        verset = CharField()

        class Meta:
            database = db

    db.connect()

    db.create_tables([Daily_2021])

    # result = get_text()
    for month in range(1,13):
        for day in range(1, get_month_days(month) + 1):
            result = get_text(month, day)
            print(f"{month} {day} {result[0]} {result[1]}")
            Daily_2021.create(
                month=month,
                day=day,
                text=result[0],
                verset=result[1]
            )
        print()



    # print(result[0])
    # print(f"—{result[1]}")


if __name__ == '__main__':
    main()
