# SPDX-FileCopyrightText: 2022 Free Software Foundation Europe <contact@fsfe.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid
from datetime import datetime
from typing import List, Optional

import fingerprints
from lxml import etree

from tedective_etl.schema import ocds
from tedective_etl.ted_to_ocds import extractors, trackers

implemented_forms = ["F01", "F02", "F03"]


def ted_notice_to_ocds_releases(
    doc_id: str,
    ted_url: str,
    form_type: str,
    ocid_prefix: str,
    object_contract: List[etree._Element],
    doc_sec_coded: etree._Element,
    doc_sec_forms: etree._Element,
    doc_sec_trans: etree._Element,
    translate_from: Optional[str] = None,
) -> tuple():
    """
    Returns a list of OCDS releases from the XML source of TED notices.
    See https://standard.open-contracting.org/profiles/eu/latest/en/forms/F01/
    for more information.

    :param form_type:
    :param ocid_prefix:
    :param doc_id:
    :param ted_url:
    :param object_contract:
    :param doc_sec_forms:
    :param doc_sec_coded:
    :param doc_sec_trans:
    :param translate_from:
    :rtype:
    """
    releases = []
    organizations = []

    # Only process implemented form types
    if form_type not in implemented_forms:
        return releases, organizations

    # A simple counter to keep track of the number of elements in one '/OBJECT_CONTRACT'
    elem_count = 0

    # Generate an OCDS release for each '/OBJECT_CONTRACT' element
    elem: etree._Element
    for elem in object_contract:
        elem_count += 1

        # Generate OCID
        if form_type == "F01" and len(object_contract) == 1:
            # If it's an F01 form and there is only one '/OBJECT_CONTRACT' element,
            # generate an OCID based on 'DOC_ID'
            id = doc_id
            ocid = ocid_prefix + str(uuid.uuid5(uuid.NAMESPACE_URL, doc_id))
        elif form_type == "F01" and len(object_contract) > 1:
            # There are more than one '/OBJECT_CONRACT' elements, for each of which a
            # new release with a new OCID needs to be generated, so use the counter
            id = f"{doc_id}-{elem_count}"
            ocid = ocid_prefix + str(
                uuid.uuid5(uuid.NAMESPACE_URL, f"{doc_id}-{elem_count}")
            )
        elif form_type == "F02" or form_type == "F03":
            # If it's an F02 form or an F03 form, first check whether there are
            # related documents.
            related_doc_id = extractors.extract_text(
                doc_sec_forms, ".//PROCEDURE/NOTICE_NUMBER_OJ"
            )
            if related_doc_id is not None:
                trackers.related_doc_id_count += 1
            # If there are related documents, generate an OCID based on the
            # existing document ID
            if related_doc_id is not None:
                if len(object_contract) > 1:
                    id = f"{doc_id}-{elem_count}"
                    ocid = ocid_prefix + str(
                        uuid.uuid5(uuid.NAMESPACE_URL, f"{related_doc_id}-{elem_count}")
                    )
                else:
                    id = doc_id
                    ocid = ocid_prefix + str(
                        uuid.uuid5(uuid.NAMESPACE_URL, related_doc_id)
                    )
            else:
                if len(object_contract) > 1:
                    id = f"{doc_id}-{elem_count}"
                    ocid = ocid_prefix + str(
                        uuid.uuid5(uuid.NAMESPACE_URL, f"{doc_id}-{elem_count}")
                    )
                else:
                    id = doc_id
                    ocid = ocid_prefix + str(uuid.uuid5(uuid.NAMESPACE_URL, doc_id))
        else:
            id = doc_id
            ocid = ocid_prefix

        # Retrieve date when Release was published
        date =  datetime.strptime(
                    doc_sec_coded.find(".//DATE_PUB", namespaces=doc_sec_coded.nsmap).text,
                    "%Y%m%d",  # type: ignore
        )

        # Define Release object instance and set some initial values
        release = ocds.Release(
            id=id,
            ocid=ocid,
            language="en",
            date=date,
            initiationType=ocds.InitiationType.tender,
            tag=[ocds.TagEnum.tender],
            tedURL=ted_url,
        )

        # Define linked objects and optionally set some defaults
        # II.1.1
        # tender_id = extractors.extract_text(elem, ".//REFERENCE_NUMBER")
        # if not tender_id:
        #     tender_id = release.id
        tender = ocds.Tender(
            # TODO This should be checked for tender ID: /OBJECT_CONTRACT/REFERENCE_NUMBER
            id=str(uuid.uuid4()),
            legalBasis=ocds.Classification(scheme="CELEX"),
        )
        release.tender = tender

        # F01
        if form_type == "F01":
            # https://standard.open-contracting.org/profiles/eu/latest/en/forms/F01/#preamble
            notice_type = doc_sec_forms.find(  # type: ignore
                ".//NOTICE", namespaces=doc_sec_forms.nsmap
            ).get("TYPE")
            if notice_type == "PRI_ONLY" or notice_type == "PRI_REDUCING_TIME_LIMITS":
                release.tag = [ocds.TagEnum.planning]
                tender.status = ocds.Status.planned
            if notice_type == "PRI_CALL_COMPETITION":
                release.tag = [ocds.TagEnum.planning, ocds.TagEnum.tender]
                tender.status = ocds.Status.active

        # F02
        elif form_type == "F02":
            tender.status = ocds.Status.active

        # F03
        elif form_type == "F03":
            release.tag = [ocds.TagEnum.award, ocds.TagEnum.contract]
            tender.status = ocds.Status.complete

        # Section I - Contracting Authority (CA)
        # https://standard.open-contracting.org/profiles/eu/latest/en/forms/F01/#section-i
        # I.1 Name and addresses
        buyer_name = extractors.extract_text(
            doc_sec_forms,
            ".//CONTRACTING_BODY/ADDRESS_CONTRACTING_BODY/OFFICIALNAME",
        )

        buyer_identifier = ocds.Identifier(legalName=buyer_name)
        buyer_identifier.id = extractors.extract_text(
            doc_sec_forms,
            ".//CONTRACTING_BODY/ADDRESS_CONTRACTING_BODY/NATIONALID",
        )
        buyer_identifier.scheme = "National-ID"

        buyer_address = extractors.extract_buyer_address(doc_sec_forms)
        buyer_contactPoint = extractors.extract_buyer_contact_point(doc_sec_forms)
        buyer_details = extractors.extract_buyer_details(doc_sec_forms)

        # Generate a heavily-scrubbed fingerprint from the organization's name
        buyer_fingerprint = fingerprints.generate(buyer_name)
        # Generate UUID based on that fingerprint. Same fingerprint, same UUID.
        try:
            buyer_uuid = uuid.uuid5(uuid.NAMESPACE_URL, buyer_fingerprint)
        except TypeError:
            buyer_uuid = uuid.uuid4()
        buyer = ocds.Organization(
            id=str(buyer_uuid),
            name=buyer_name,
            identifier=buyer_identifier,
            address=buyer_address,
            contactPoint=buyer_contactPoint,
            details=buyer_details,
            roles={"buyer"},
        )
        # Add the organization to the list of organizations
        organizations.append(buyer)

        # Add the buyer to the release
        release.buyer = buyer

        # Add the buyer to the list of parties
        release.parties = set()
        release.parties.add(buyer)

        # Look for additional buyer
        additional_buyer = doc_sec_forms.find(
            ".//CONTRACTING_BODY/ADDRESS_CONTRACTING_BODY_ADDITIONAL",
            namespaces=doc_sec_forms.nsmap,
        )
        if additional_buyer is not None:
            add_buyer_name = extractors.extract_text(
                doc_sec_forms,
                ".//CONTRACTING_BODY/ADDRESS_CONTRACTING_BODY_ADDITIONAL/OFFICIALNAME",
            )

            add_buyer_identifier = ocds.Identifier(legalName=add_buyer_name)
            add_buyer_identifier.id = extractors.extract_text(
                doc_sec_forms,
                ".//CONTRACTING_BODY/ADDRESS_CONTRACTING_BODY_ADDITIONAL/NATIONALID",
            )
            add_buyer_identifier.scheme = "National-ID"

            add_buyer_address = extractors.extract_buyer_address(
                doc_sec_forms, "ADDRESS_CONTRACTING_BODY_ADDITIONAL"
            )
            add_buyer_contactPoint = extractors.extract_buyer_contact_point(
                doc_sec_forms, "ADDRESS_CONTRACTING_BODY_ADDITIONAL"
            )
            # Generate a heavily-scrubbed fingerprint from the organization's name
            add_buyer_fingerprint = fingerprints.generate(add_buyer_name)
            # Generate UUID based on that fingerprint. Same fingerprint, same UUID.
            add_buyer_uuid = uuid.uuid5(uuid.NAMESPACE_URL, add_buyer_fingerprint)
            add_buyer = ocds.Organization(
                id=str(add_buyer_uuid),
                fingerprint=add_buyer_fingerprint,
                name=add_buyer_name,
                identifier=add_buyer_identifier,
                address=add_buyer_address,
                contactPoint=add_buyer_contactPoint,
                roles={"buyer"},
            )
            if add_buyer_uuid == buyer_uuid:
                # Additional buyer is the same as primary buyer, do nothing
                pass
            else:
                # Additional buyer is new, add to lists
                organizations.append(add_buyer)
                release.parties.add(add_buyer)

        # I.2 Information about joint procurement
        cb_pl = doc_sec_forms.find(
            ".//CONTRACTING_BODY/PROCUREMENT_LAW", namespaces=doc_sec_forms.nsmap
        )
        if cb_pl is not None:
            tender.crossBorderLaw = cb_pl[0].text
        cp = doc_sec_forms.find(
            ".//CONTRACTING_BODY/CENTRAL_PURCHASING", namespaces=doc_sec_forms.nsmap
        )
        if cp is not None:
            buyer.roles.append("centralPurchasingBody")

        # TODO I.3 Communication
        cb_url_p = doc_sec_forms.find(
            ".//CONTRACTING_BODY/URL_PARTICIPATION", namespaces=doc_sec_forms.nsmap
        )
        if cb_url_p is not None:
            tender.submissionMethod = ["electronicSubmission"]
            tender.submissionMethodDetails = cb_url_p.text

        classifications = []
        # I.4 Type of the contracting authority
        buyer_details_classification = ocds.Classification(
            scheme="TED_CA_TYPE",
            id=str(
                extractors.extract_attribute(
                    doc_sec_forms, ".//CONTRACTING_BODY/CA_TYPE", "VALUE"
                )
            ),
            # TODO Add description
        )
        if buyer_details_classification.id is not None:
            classifications.append(buyer_details_classification)

        # I.5 Main activity
        buyer_details_main_activity = ocds.Classification(
            scheme="COFOG",
            id=extractors.extract_attribute(
                doc_sec_forms, ".//CONTRACTING_BODY/CA_ACTIVITY", "VALUE"
            ),
        )
        if buyer_details_main_activity.id is not None:
            classifications.append(buyer_details_main_activity)

        if len(classifications) > 0:
            buyer.details["classifications"] = classifications

        # Section II
        # https://standard.open-contracting.org/profiles/eu/latest/en/forms/F01/#section-ii
        # II.1 Scope of the procurement
        # II.1.1 Title
        tender.title = extractors.extract_title(elem, doc_sec_trans)

        # II.1.2 Main CPV Code
        classification = ocds.Classification(
            scheme="CPV", id=extractors.extract_attribute(elem, ".//CPV_CODE", "CODE")
        )
        tender.classification = classification

        # TODO II.1.3
        # II.1.4 Short description
        tender.description = extractors.extract_description(elem)

        # II.1.5 Estimated Total Value
        tender.value = extractors.extract_value(doc_sec_forms, "tender", date)

        # Section V - Award of contract
        if form_type == "F03":
            # Check if there are more awards
            award_elems = doc_sec_forms.findall(
                ".//AWARD_CONTRACT", namespaces=doc_sec_forms.nsmap
            )
            release.awards = set()
            award_elem: etree._Element
            for award_elem in award_elems:
                award_id = uuid.uuid4()
                award_title = extractors.extract_title(award_elem, doc_sec_trans)
                award = ocds.Award(id=str(award_id), title=award_title)

                if extractors.extract_text(award_elem, ".//AWARDED_CONTRACT"):
                    award.status = ocds.AwardStatus.active
                    award_date = datetime.strptime(
                        extractors.extract_text(
                            award_elem,
                            ".//DATE_CONCLUSION_CONTRACT",
                        ),
                        "%Y-%m-%d",
                    )
                    contract = ocds.Contract(
                        id=str(uuid.uuid4()),
                        awardID=str(award_id),
                        title=award_title,
                        description=None,
                        status=ocds.ContractStatus("active"),
                        period=None,
                        value=extractors.extract_value(award_elem, "award", award_date),
                        items=None,
                        dateSigned=award_date,
                        documents=None,
                    )
                    release.contracts = set()
                    release.contracts.add(contract)
                else:
                    award.status = ocds.AwardStatus.unsuccessful

                # V.2.3 Name and address of the contractor(s)
                supplier_elems = award_elem.findall(
                    ".//CONTRACTOR",
                    namespaces=award_elem.nsmap,
                )

                for supplier_elem in supplier_elems:
                    supplier_name = extractors.extract_text(
                        supplier_elem, ".//OFFICIALNAME"
                    )
                    supplier_fingerprint = fingerprints.generate(supplier_name)
                    try:
                        supplier_id = uuid.uuid5(
                            uuid.NAMESPACE_URL, supplier_fingerprint
                        )
                    except TypeError:
                        supplier_id = uuid.uuid4()
                    supplier = ocds.Organization(
                        id=str(supplier_id),
                        name=supplier_name,
                        fingerprint=supplier_fingerprint,
                        identifier=ocds.Identifier(
                            id=extractors.extract_text(supplier_elem, ".//NATIONALID"),
                            scheme="National-ID",
                            legalName=supplier_name,
                        ),
                        roles={"supplier"},
                        address=extractors.extract_supplier_address(supplier_elem),
                    )

                    award.suppliers = set()
                    award.suppliers.add(supplier)

                    # This is a new supplier
                    release.parties.add(supplier)

                    # Add supplier to list of organizations
                    organizations.append(supplier)

                    # iterated through all suppliers for award

                # Add award to release
                release.awards.add(award)
                # iterated through all awards

        if release not in releases:
            releases.append(release)
        # End of for-loop through '/OBJECT_CONTRACT'

    # After having iterated through all '/OBJECT_CONTRACT' elements, return releases
    return releases, organizations
