#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Free Software Foundation Europe <contact@fsfe.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import tarfile
from calendar import monthrange
from datetime import datetime
from glob import glob
from typing import Any, List, Optional

from dateutil import rrule
from lxml import etree

from tedective_etl.ted_to_ocds.transform import ted_notice_to_ocds_releases

log = logging.getLogger()


def extract_ted_notices(in_dir, year_month):
    """
    Extracts TED XMLs for a given year and month.

    Args:
        in_dir (str): Directory where TED XML files are stored
        year_month (str): Year and month to extract

    Returns:
        None
    """
    log.info(f"Extracting TED XMLs for {year_month}...")
    f_to_extract = tarfile.open(f"{in_dir}/{year_month}.tar.gz")
    f_to_extract.extractall(f"{in_dir}/{year_month}")
    os.remove(f"{in_dir}/{year_month}.tar.gz")


def get_ted_xml_files(
    in_dir: str,
    first_month: str = "2017-01",
    last_month: Optional[str] = None,
) -> dict:
    """
    Generates a dictionary of lists of TED XML filepaths from a given directory

    Args:
        in_dir (str): Directory where TED XML files are stored
        first_month (str): First month to get XML files for
        last_month (str): Last month to get XML files for

    Returns:
        dict: Dictionary of lists of TED XML filepaths from a given directory.
        The key for each list of XML filepaths is the date in the format
        'YYYYMMDD'.
    """
    xml_dict = dict()
    start_date = datetime(
        int(first_month.split("-")[0]),
        int(first_month.split("-")[1]),
        1,
    )

    if last_month is None:
        # Define end_date as the current date
        end_date = datetime.now().strftime("%Y-%m")
    else:
        end_date = last_month

    end_year = int(end_date.split("-")[0])
    end_month = int(end_date.split("-")[1])

    # Get the last day of the month
    _, last_day = monthrange(end_year, end_month)
    end_date = datetime(end_year, end_month, last_day)

    for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
        year_month = dt.strftime("%Y-%m")
        year_month_day = dt.strftime("%Y%m%d")
        xml_dict[year_month_day] = []
        for filename in glob(f"{in_dir}/{year_month}/{year_month_day}*/*.xml"):
            xml_dict[year_month_day].append(filename)

    # Remove empty lists
    xml_dict = {k: v for k, v in xml_dict.items() if v}

    return xml_dict


def process_ted_notice(xml_filepath: str) -> tuple:
    """
    Returns a dict containing the form type and the list of OCDS releases
    generated from it.

    Args:
        xml_filepath (str): Filepath of the TED XML file to process

    Returns:
        dict: Dictionary containing the form type ('form_type'), the list of
        OCDS releases ('releases'), and the list of organizations
        ('organizations') generated from the TED XML file.
    """

    # Optimize performance for XMLParser
    parser = etree.XMLParser(ns_clean=True, huge_tree=True, remove_blank_text=True)

    # Define tree and generate cleaned root of XML
    tree: etree._ElementTree[Any] = etree.parse(xml_filepath, parser)  # type: ignore
    root: etree._Element = tree.getroot()

    # Define sections based on list indices
    # sec_techn = root[0]
    # sec_links = root[1]
    sec_coded: etree._Element = root[2]
    sec_trans = root[3]
    sec_forms = root[4]

    # This is the notice ID,
    try:
        sec_coded.find(".//NOTICE_DATA/NO_DOC_OJS", namespaces=sec_coded.nsmap).text

    except AttributeError:
        # TODO Implement eForms
        return {"form_type": "eForm", "releases": [], "organizations": []}

    # URI of current TED notice
    doc_id_short = root.get("DOC_ID")
    ted_url = f"https://ted.europa.eu/udl?uri=TED:NOTICE:{doc_id_short}:TEXT:EN:HTML"

    # Define form type
    form_type = sec_forms[0].get("FORM")
    form_version = sec_forms[0].get("VERSION")
    if form_type is None:
        try:
            form_type = sec_forms[1].get("FORM")
            form_version = sec_forms[1].get("VERSION")
            if form_type is None:
                return {"form_type": "invalid", "releases": [], "organizations": []}
        except IndexError:
            if form_version is None:
                return {"form_type": "invalid", "releases": [], "organizations": []}
            else:
                return {"form_type": form_version, "releases": [], "organizations": []}
    if form_type[0].isdigit():
        if len(form_type) == 1:
            form_type = f"F0{form_type}"
        else:
            form_type = f"F{form_type}"

    # Prune 'sec_forms' to only contain English version or if that is not available,
    # another language version. The language from which translation will be needed is
    # also passed
    translate_from = None
    for elem in sec_forms:
        if elem.tag.endswith("NOTICE_UUID"):
            continue
        lang: str = elem.get("LG")
        if lang == "EN":
            new_sec_forms: etree._Element = elem
            # Found an English form; stop iterating
            break
        # No English form was found. Translation will be needed
        new_sec_forms = elem
        translate_from = lang.lower()

    sec_forms = new_sec_forms

    # Check if 'OBJECT_CONTRACT' is indeed a list. If the list contains more than
    # one item, then multiple releases need to be generated.
    object_contract: List = sec_forms.findall(
        ".//OBJECT_CONTRACT", namespaces=sec_forms.nsmap
    )
    assert isinstance(object_contract, List)

    # Pass off to OCDS parser to generate releases
    result = ted_notice_to_ocds_releases(
        # Use doc_id_short as ID as its URL-safe
        doc_id=doc_id_short,
        ted_url=ted_url,
        form_type=form_type,
        ocid_prefix="ocds-jyvdv7-",
        object_contract=object_contract,
        doc_sec_forms=sec_forms,
        doc_sec_coded=sec_coded,
        doc_sec_trans=sec_trans,
        translate_from=translate_from,
    )

    # Construct the dictionary
    processed_ted_notice = {
        "form_type": form_type,
        "releases": result[0],
        "organizations": result[1],
    }
    return processed_ted_notice
