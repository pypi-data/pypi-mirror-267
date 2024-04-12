import urllib

import fingerprints
import numpy
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import splink.duckdb.comparison_template_library as ctl
from pyarrow import json  # noqa: F401
from splink.duckdb.blocking_rule_library import block_on
from splink.duckdb.comparison_library import exact_match
from splink.duckdb.linker import DuckDBLinker


def dedupe_organizations(path_organization_json: str, path_output: str):
    # Load the .jsonl file produced by the parser to parquet table
    table = pa.json.read_json(path_organization_json)

    # Load df from table
    df = table.to_pandas()

    # Normalise 'identifier' column
    identifier = pd.json_normalize(df["identifier"])
    identifier = identifier.add_prefix("identifier_")

    # Normalise 'address' column
    address = pd.json_normalize(df["address"])
    address = address.add_prefix("address_")

    # Normalise 'contactPoint' column
    contactPoint = pd.json_normalize(df["contactPoint"])
    contactPoint = contactPoint.add_prefix("contactPoint_")

    # Normalise 'details' column
    details = pd.json_normalize(df["details"])
    details = details.add_prefix("details_")

    # Concatenate the normalised columns to the original df
    df = pd.concat([df, identifier, address, contactPoint, details], axis=1)

    # Some more mangling
    df["roles"] = df["roles"].apply(lambda x: x[0] if x.any() else None)
    df["details_classification_tedcatype"] = df["details_classifications"].apply(
        lambda x: x[0]["id"] if isinstance(x, numpy.ndarray) and x.any() else None
    )
    df["details_classification_cofog"] = df["details_classifications"].apply(
        lambda x: x[1]["id"] if isinstance(x, numpy.ndarray) and len(x) > 1 else None
    )

    # Normalize the 'name' column using fingerprints
    df["name"] = df["name"].apply(lambda x: fingerprints.generate(x))
    # Case: Dataport AÖR
    df["name"] = df["name"].apply(
        lambda x: "dataport aor" if isinstance(x, str) and "dataport" in x else x
    )

    # Clean the 'details_url' column using urllib.parse and only return hostname and path
    df["details_url"] = df["details_url"].apply(
        lambda x: None if not isinstance(x, str) else urllib.parse.urlparse(x).hostname
    )

    # Drop the original columns
    df = df.drop(
        [
            "identifier",
            "address",
            "contactPoint",
            "details",
            "additionalIdentifiers",
            "contactPoint_url",
            "identifier_scheme",
            "identifier_legalName",
            "details_classifications",
        ],
        axis=1,
    )

    # Replace all None values with NaN
    df = df.replace({None: numpy.nan})

    # Set up the linker
    settings = {
        "link_type": "dedupe_only",
        "unique_id_column_name": "id",
        "blocking_rules_to_generate_predictions": [
            block_on("name"),
            block_on("substr(name, 1, 12)"),
            block_on("substr(contactPoint_email, 1, 10)"),
            block_on("contactPoint_name"),
            block_on("contactPoint_telephone"),
            block_on("contactPoint_faxNumber"),
            block_on("details_url"),
            block_on(["substr(address_streetAddress, 1, 6)", "address_region"]),
            block_on(["identifier_id", "address_countryName"]),
            block_on(["substr(name, 1, 6)", "address_region"]),
            block_on(
                [
                    "details_classification_tedcatype",
                    "details_classification_cofog",
                    "address_region",
                ]
            ),
        ],
        "comparisons": [
            ctl.name_comparison("name", term_frequency_adjustments=True),
            ctl.name_comparison("contactPoint_name", term_frequency_adjustments=True),
            ctl.email_comparison("contactPoint_email", include_domain_match_level=True),
            ctl.postcode_comparison("address_postalCode"),
            exact_match("address_streetAddress"),
            exact_match("identifier_id"),
            exact_match("details_url"),
            exact_match(
                "details_classification_tedcatype", term_frequency_adjustments=True
            ),
            exact_match(
                "details_classification_cofog", term_frequency_adjustments=True
            ),
        ],
    }
    linker = DuckDBLinker(df, settings)

    # Estimate the parameters of the model
    linker.estimate_probability_two_random_records_match(
        [block_on(["contactPoint_name"])], recall=0.8
    )
    linker.estimate_u_using_random_sampling(max_pairs=1e7)
    linker.estimate_parameters_using_expectation_maximisation(
        block_on(["contactPoint_name"]),
        estimate_without_term_frequencies=True,
    )

    # Predict the matches and convert the mathces with a probability above 0.2
    # to a pandas dataframe
    df_predict = linker.predict(threshold_match_probability=0.2)
    df_predict = df_predict.as_pandas_dataframe()

    # Create a new dataframe with only the needed columns
    df_result = df_predict[["id_l", "id_r", "match_probability"]]

    # Rename those columns
    df_result = df_result.rename(columns={"id_l": "from", "id_r": "to"})

    # Remove all rows where match_probability is below 0.5 and remove the index
    df_result = df_result[df_result["match_probability"] > 0.1]
    df_result = df_result.reset_index(drop=True)

    # Write df_result to a parquet file in the output folder and name it
    # 'edges_isSameAs.parquet'
    table = pa.Table.from_pandas(df_result)
    pq.write_table(table, f"{path_output}/edges_isSameAs.parquet")
