# SPDX-FileCopyrightText: 2023 Free Software Foundation Europe <contact@fsfe.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
from datetime import date, datetime
from functools import cache
from pathlib import Path
from typing import Optional

import ftfy
import orjson
from _decimal import Decimal

from tedective_etl.schema import ocds


def get_project_root() -> Path:
    """
    Get the root directory of the project.

    Returns:
        Path: The root directory of the project.

    """
    if os.path.exists("/.dockerenv"):
        return Path("/app")
    return Path(__file__).parent.parent


def ocds_json_serializer(obj):
    """Custom JSON serializer for database insertion"""
    if isinstance(
        obj,
        (
            ocds.TagEnum,
            ocds.InitiationType,
            ocds.Status,
            ocds.ProcurementMethod,
            ocds.MainProcurementCategory,
            ocds.AwardStatus,
            ocds.ContractStatus,
            ocds.MilestoneStatus,
            ocds.Currency,
        ),
    ):
        return str(obj)
    # elif issubclass(type(obj), .SQLModel):
    # This allows quick and dirty insertion of JSON into models
    #    return obj.__dict__
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()


@cache
def clean(string: str) -> str:
    """
    Clean a string by removing extra whitespace and fixing unicode.

    Args:
        string (str): The string to clean.

    Returns:
        str: The cleaned string.

    """
    try:
        string = re.sub(r"\s+", " ", string)
        string = string.strip()
        string = ftfy.fix_text(string)
        return string
    except TypeError:
        return None


def find_closest_date(target_date, dates):
    # target_date = datetime.strptime(target_date, "%Y-%m-%d")
    closest_date = min(dates, key=lambda date: abs(datetime.strptime(date, "%Y-%m-%d") - target_date))
    return closest_date


def load_closest(date: str) ->dict:
    root = "/tmp" #get_project_root()
    path = os.path.join(root, "ted_currencies/rates.json")

    with open(path, "rb") as file:
        rates = orjson.loads(file.read())

    closest_date = find_closest_date(date, rates.keys()) 
    closest_rates= rates[closest_date]

    return closest_rates


def request_currency(amount: str, currency: str, date: str) -> Decimal:
    rates = load_closest(date)

    if currency in rates:
        rate = Decimal(rates[currency])
        amountEur = round(Decimal(amount) / rate)

        return amountEur
    else:
        return None


@cache
def convert_to_euro(amount: str, currency: str, date: str) -> Optional[Decimal]:
    return request_currency(amount, currency, date)


def prune_list(list_of_objects, seen_ids):
    """
    Prunes a list of objects by removing duplicates.

    Args:
        list_of_objects (list): The list of objects to prune.
        seen_ids (set): A set of ids that have already been seen.

    Returns:
        list: The pruned list of objects.
        set: The updated set of ids that have already been seen.

    """
    filtered_list = []
    ids = seen_ids
    for obj in list_of_objects:
        if type(obj) == ocds.Organization and obj.id not in ids:
            filtered_list.append(obj)
            ids.add(obj.id)
        elif type(obj) == ocds.Organization and obj.id in ids:
            continue
        else:
            filtered_list.append(obj)

    return list(set(filtered_list)), seen_ids
