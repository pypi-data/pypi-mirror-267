# SPDX-FileCopyrightText: 2023 Free Software Foundation Europe <contact@fsfe.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Optional

import ftfy
import phonenumbers
from _decimal import Decimal
from lxml import etree

from tedective_etl.schema import ocds
from tedective_etl.utils import clean, convert_to_euro


def extract_title(
    elem: etree._Element,
    doc_sec_trans: etree._Element,
) -> Optional[str]:
    if elem.find(".//TITLE", namespaces=elem.nsmap) is None:
        return [
            doc.find(".//TI_TEXT", namespaces=elem.nsmap)[0].text
            for doc in doc_sec_trans.iterfind(".//ML_TI_DOC", namespaces=elem.nsmap)
            if doc.get("LG") == "EN"
        ][0]

    orig_title = elem.find(".//TITLE", namespaces=elem.nsmap).text
    if not orig_title:
        orig_title = elem.find(".//TITLE", namespaces=elem.nsmap)[0].text

    if doc_sec_trans is None:
        return clean(orig_title)

    else:
        try:
            title = (
                [
                    doc.find(".//TI_TEXT", namespaces=elem.nsmap)[0].text
                    for doc in doc_sec_trans.iterfind(
                        ".//ML_TI_DOC", namespaces=elem.nsmap
                    )
                    if doc.get("LG") == "EN"
                ][0]
                + " ["
                + orig_title
                + "]"
            )
            return clean(title)
        except TypeError:
            return orig_title


def extract_description(elem: etree._Element) -> str:
    description = elem.find(".//SHORT_DESCR", namespaces=elem.nsmap)[0].text
    return clean(description)


def extract_text(elem: etree._Element, path: str) -> Optional[str]:
    try:
        to_return = elem.find(path, namespaces=elem.nsmap).text
        return ftfy.fix_text(to_return)
    except TypeError:
        to_return = elem.find(path, namespaces=elem.nsmap)[0].text
        try:
            return ftfy.fix_text(to_return)
        except TypeError:
            return None
    except AttributeError:
        return None


def extract_buyer_contact_point(
    elem: etree._Element, buyer_search_str: Optional[str] = "ADDRESS_CONTRACTING_BODY"
) -> ocds.ContactPoint:
    name = extract_text(elem, f".//CONTRACTING_BODY/{buyer_search_str}/CONTACT_POINT")
    phone_unformatted = extract_text(
        elem, f".//CONTRACTING_BODY/{buyer_search_str}/PHONE"
    )
    if phone_unformatted:
        if "/" in phone_unformatted:
            phone_unformatted = phone_unformatted.split("/")[0]
        try:
            phonenumber = phonenumbers.parse(phone_unformatted)
            phone = phonenumbers.format_number(
                phonenumber, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            phone = phone_unformatted + " [likely invalid]"
    else:
        phone = None
    email = extract_text(elem, f".//CONTRACTING_BODY/{buyer_search_str}/E_MAIL")
    fax_unformatted = extract_text(elem, f".//CONTRACTING_BODY/{buyer_search_str}/FAX")
    if fax_unformatted:
        try:
            faxnumber = phonenumbers.parse(fax_unformatted)
            fax = phonenumbers.format_number(
                faxnumber, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
        except phonenumbers.phonenumberutil.NumberParseException:
            fax = fax_unformatted + " [likely invalid]"
    else:
        fax = None

    url = extract_text(elem, f".//CONTRACTING_BODY/{buyer_search_str}/URL_GENERAL")
    return ocds.ContactPoint(
        name=name, telephone=phone, email=email, faxNumber=fax, url=url
    )


def extract_buyer_details(
    elem: etree._Element, buyer_search_str: Optional[str] = "ADDRESS_CONTRACTING_BODY"
) -> Dict:
    url = extract_text(elem, f".//CONTRACTING_BODY/{buyer_search_str}/URL_GENERAL")
    buyerProfile = extract_text(
        elem, f".//CONTRACTING_BODY/{buyer_search_str}/URL_BUYER"
    )
    return {"url": url, "buyerProfile": buyerProfile}


def extract_buyer_address(
    elem: etree._Element,
    base_path: Optional[str] = "CONTRACTING_BODY",
    search_path: Optional[str] = "ADDRESS_CONTRACTING_BODY",
) -> ocds.Address:
    # TODO Think about using libpostal here for normalizing
    streetAddress = extract_text(elem, f".//{base_path}/{search_path}/ADDRESS")
    locality = extract_text(elem, f".//{base_path}/{search_path}/TOWN")
    postalCode = extract_text(elem, f".//{base_path}/{search_path}/POSTAL_CODE")

    try:
        region = elem.find(
            f".//{base_path}/{search_path}" + "/{*}NUTS", namespaces=elem.nsmap
        ).get("CODE")
    except AttributeError:
        region = None

    try:
        countryName = elem.find(
            f".//{base_path}/{search_path}/COUNTRY",
            namespaces=elem.nsmap,
        ).get("VALUE")
    except AttributeError:
        # TODO Do proper mapping to country names here
        if region:
            countryName = region[:2]
        else:
            countryName = None

    return ocds.Address(
        streetAddress=streetAddress,
        locality=locality,
        region=region,
        postalCode=postalCode,
        countryName=countryName,
    )


def extract_supplier_address(
    elem: etree._Element,
) -> ocds.Address:
    # TODO Think about using libpostal here for normalizing
    streetAddress = extract_text(elem, ".//ADDRESS")
    locality = extract_text(elem, ".//TOWN")
    postalCode = extract_text(elem, ".//POSTAL_CODE")

    try:
        region = elem.find(".//{*}NUTS", namespaces=elem.nsmap).get("CODE")
    except AttributeError:
        region = None

    try:
        countryName = elem.find(
            ".//COUNTRY",
            namespaces=elem.nsmap,
        ).get("VALUE")
    except AttributeError:
        if region:
            countryName = region[:2]
        else:
            countryName = None

    return ocds.Address(
        streetAddress=streetAddress,
        locality=locality,
        region=region,
        postalCode=postalCode,
        countryName=countryName,
    )


def _extract_value(elem: etree._Element, path: str, date) -> Optional[ocds.Value]:
    amount = extract_text(elem, path)
    currency = extract_attribute(elem, path, "CURRENCY")
    amountEur = None
    if amount is not None:
        if currency != "EUR":
            amountEur = convert_to_euro(amount=amount, currency=currency, date=date)
        else:
            # amount = float(Decimal(amount))
            amountEur = amount
        return ocds.Value(
            amount=float(Decimal(amount)),
            currency=ocds.Currency[currency],
            amountEur=amountEur,
        )
    else:
        return None


def extract_value(elem: etree._Element, ocds_object: str, date: str = None) -> Optional[ocds.Value]:
    # TODO Update currency conversion without re-ingesting all the data

    if ocds_object == "tender":
        tender_value_paths = [
            ".//OBJECT_CONTRACT/VAL_ESTIMATED_TOTAL",
        ]

        for path in tender_value_paths:
            value = _extract_value(elem, path, date)
            if value is not None:
                return value
            else:
                continue

    elif ocds_object == "award":
        award_value_paths = [
            ".//VAL_TOTAL",
            ".//VALUES/VAL_TOTAL",
        ]

        for path in award_value_paths:
            value = _extract_value(elem, path, date)
            if value is not None:
                return value
            else:
                continue


def extract_attribute(elem: etree._Element, path: str, attribute: str) -> Optional[str]:
    try:
        to_return = elem.find(path, namespaces=elem.nsmap).get(attribute)
        return ftfy.fix_text(to_return)
    except AttributeError:
        return None
