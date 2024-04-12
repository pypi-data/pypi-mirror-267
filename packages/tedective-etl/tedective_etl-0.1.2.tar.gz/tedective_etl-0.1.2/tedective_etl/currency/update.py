# SPDX-FileCopyrightText: 2024 Free Software Foundation Europe <contact@fsfe.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import calendar
import os

import orjson
import requests


def api_request(start_date: str, end_date: str) -> dict:
    host = "api.frankfurter.app"
    url = f'https://{host}/{start_date}..{end_date}'
    response = requests.get(url)
    rates = response.json()
    return rates["rates"]


def get_last_day_of_month(date_str):
    year, month = map(int, date_str.split('-'))
    _, last_day = calendar.monthrange(year, month)
    return last_day


def fetch_exchange_rates(start_date: str, end_date: str):
    start_date = start_date + "-01"
    end_date = end_date + "-" + str(get_last_day_of_month(end_date))
    rates = api_request(start_date, end_date)
    
    root = "/tmp" #get_project_root()
    dest = os.path.join(root, "ted_currencies")
    dest_file = os.path.join(dest, "rates.json")

    if not os.path.exists(dest):
        os.makedirs(dest)

    with open(dest_file, "wb") as file:
        file.write(orjson.dumps(rates, option=orjson.OPT_INDENT_2))
