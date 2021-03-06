# General imports
from __future__ import annotations  # Enables self-referencing type hints, not needed in python 4.0+
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from datetime import date
from calendar import HTMLCalendar
from pkg_resources import resource_string
from os.path import dirname
from os.path import realpath

# Project imports
from .utils import Color

library_path = dirname(realpath(__file__))


class DayOfTheWeek(Enum):
    """
    Helper utility to consolidate state
    """
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def title(self) -> str:
        return self.name.title()

    def lower(self) -> str:
        return self.name.lower()

    def upper(self) -> str:
        return self.name.upper()

    def __str__(self):
        return self.lower()

    @staticmethod
    def from_name(current_day: str) -> DayOfTheWeek:
        return DayOfTheWeek[current_day.upper()]


class Month(Enum):
    """
    A nice helper utility, since there's a lot of different
    ways that month state representation occurs thanks to
    calls to other libraries, so we create this to refer
    to a single state, and just call the relevant presentation
    method that's required.
    """
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def title(self) -> str:
        return self.name.title()

    @staticmethod
    def from_name(current_month_name: str) -> Month:
        return Month[current_month_name.upper()]


@dataclass(order=True, frozen=True)
class WeeklyPage:
    """
    A class representing all data required to template
    a single page in the weekly planner
    """
    year: int
    month: Month

    first_day: date
    second_day: date
    third_day: date
    fourth_day: date
    fifth_day: date
    sixth_day: date
    seventh_day: date

    @property
    def calendar_image(self) -> str:
        return f"img/{self.year}-{self.month.title()}-calendar"

    @property
    def first_ordinal(self) -> str:
        return self.to_page_header(self.first_day)

    @property
    def second_ordinal(self) -> str:
        return self.to_page_header(self.second_day)

    @property
    def third_ordinal(self) -> str:
        return self.to_page_header(self.third_day)

    @property
    def fourth_ordinal(self) -> str:
        return self.to_page_header(self.fourth_day)

    @property
    def fifth_ordinal(self) -> str:
        return self.to_page_header(self.fifth_day)

    @property
    def sixth_ordinal(self) -> str:
        return self.to_page_header(self.sixth_day)

    @property
    def seventh_ordinal(self) -> str:
        return self.to_page_header(self.seventh_day)

    @staticmethod
    def to_page_header(input_date: date) -> str:
        if input_date is None:
            return "Rest day"
        return f"{to_ordinal(input_date.day)} {input_date.strftime('%A')}"


class CustomHTMLCal(HTMLCalendar):
    """
    An unfortunate byproduct of using the calendar library,
    where we need this whole particular class to enable accessing
    the title element of the calendar
    """
    cssclass_month_head = "month-head"


class CalendarImage:
    """
    Contains the actual data required to generate an image
    of the calendar via html
    """
    def __init__(self, year: int, month: Month, calendar: HTMLCalendar, primary_color: Color, secondary_color: Color):
        self.year = year
        self.month = month
        self.calendar = calendar
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    @property
    def path(self) -> Path:
        return Path(f"img/{self.year}-{self.month.title()}-calendar.png")

    @property
    def to_html(self) -> str:
        html_template = load_resource_file("calendar-template.html")
        html_template = html_template.replace("{{primary_color}}", self.primary_color.hexcode())
        html_template = html_template.replace("{{secondary_color}}", self.secondary_color.hexcode())
        html_template = html_template.replace("{{calendar}}", self.calendar.formatmonth(self.year, self.month.value))
        html_template = html_template.replace("{{font}}", f"url('file:{library_path}/resources/cmunrm.otf') format(\"opentype\")")

        # All of this because the html calendar is a piece of shit
        html_template = html_template.replace("Mon", "M")
        html_template = html_template.replace("Tue", "T")
        html_template = html_template.replace("Wed", "W")
        html_template = html_template.replace("Thu", "T")
        html_template = html_template.replace("Fri", "F")
        html_template = html_template.replace("Sat", "S")
        html_template = html_template.replace("Sun", "S")

        html_template = html_template.replace("table border=\"0\"", "table")
        html_template = html_template.replace("cellpadding=\"0\"", "")
        html_template = html_template.replace("cellspacing=\"0\"", "")

        return html_template


"""
Helper functions
"""


def to_ordinal(n: int) -> str:
    """
    See https://stackoverflow.com/a/50992575.
    Convert an integer into its ordinal representation::

    make_ordinal(0)   => '0th'
    make_ordinal(3)   => '3rd'
    make_ordinal(122) => '122nd'
    make_ordinal(213) => '213th'
    """
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def load_resource_file(file_name: str) -> str:
    return resource_string("weekly_planner.resources", file_name).decode('utf-8')
