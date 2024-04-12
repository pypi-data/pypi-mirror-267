import logging
import os
import time

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from kuzu import Connection
from pyarrow import json  # noqa: F401


def create_release_schema(conn: Connection):
    """
    Creates a schema for the Release node in KuzuDB

    Args:
        conn (Connection): The database connection object.

    Returns:
        None
    """

    # TODO Add tag as STRING[] when this is fixed:
    # https://github.com/kuzudb/kuzu/issues/2703
    conn.execute(
        """
        CREATE NODE TABLE Release(
            id STRING, 
            ocid STRING, 
            date DATE,
            initiationType STRING,
            language STRING,
            tedURL STRING,
            PRIMARY KEY (id)
        )
        """
    )


def create_organization_schema(conn: Connection):
    """
    Creates a schema for the Organization node in KuzuDB

    Args:
        conn (Connection): The database connection object.

    Returns:
        None
    """

    # Add roles as STRING[], see above
    # Add additionalIdentifiers as STRUCT[], see above
    conn.execute(
        """
        CREATE NODE TABLE Organization(
            name STRING,
            id STRING,

            roles STRING,

            identifierNationalID STRING,

            addressStreetAddress STRING,
            addressLocality STRING,
            addressRegion STRING,
            addressPostalCode STRING,            
            addressCountryName STRING,

            contactPointName STRING,
            contactPointEmail STRING,
            contactPointTelephone STRING,
            contactPointFaxNumber STRING,
            contactPointUrl STRING,

            detailsUrl STRING,

            PRIMARY KEY (id)
        )
        """
    )


def create_tender_schema(conn: Connection):
    conn.execute(
        """
        CREATE NODE TABLE Tender(
            id STRING,
            title STRING, 
            description STRING, 
            status STRING,

            valueAmount DOUBLE,
            valueAmountEur DOUBLE,
            valueCurrency STRING,

            PRIMARY KEY (id)
        )
        """
    )


def create_award_schema(conn: Connection):
    conn.execute(
        """
        CREATE NODE TABLE Award(
            id STRING,
            title STRING, 
            status STRING,
            PRIMARY KEY (id)
        )
        """
    )


def create_contract_schema(conn: Connection):
    conn.execute(
        """
        CREATE NODE TABLE Contract(
            id STRING,
            title STRING,
            status STRING,

            valueAmount DOUBLE,
            valueAmountEur DOUBLE,
            valueCurrency STRING,

            dateSigned DATE,
            PRIMARY KEY (id)
        )
        """
    )


# TODO Create planning schema
def create_planning_schema(conn: Connection):
    pass


# TODO Create implementation schema
def create_implementation_schema(conn: Connection):
    pass


def create_edge_schema(conn: Connection):
    # From Release
    conn.execute("CREATE REL TABLE hasTender(FROM Release TO Tender)")
    conn.execute("CREATE REL TABLE hasBuyer(FROM Release TO Organization)")
    conn.execute("CREATE REL TABLE hasAwards(FROM Release TO Award)")
    conn.execute("CREATE REL TABLE hasContracts(FROM Release TO Contract)")
    # conn.execute("CREATE REL TABLE hasPlanning(FROM Release TO Planning)")

    # From Contract
    conn.execute("CREATE REL TABLE issuedAgainst(FROM Contract TO Award)")
    # conn.execute("CREATE REL TABLE hasImplementation(FROM Contract TO Implementation)")

    # To Organization
    conn.execute("CREATE REL TABLE hasSuppliers(FROM Award TO Organization)")
    conn.execute("CREATE REL TABLE hasTenderers(FROM Tender TO Organization)")
    conn.execute(
        "CREATE REL TABLE isSameAs(FROM Organization TO Organization, probability DOUBLE)"
    )


def create_kuzudb_schema(conn: Connection):
    """
    Creates the schema for KuzuDB

    Args:
        conn (Connection): The database connection object.

    Returns:
        None
    """
    # Create node schemas
    create_release_schema(conn)
    create_organization_schema(conn)
    create_tender_schema(conn)
    create_award_schema(conn)
    create_contract_schema(conn)
    # create_planning_schema(conn)
    # create_implementation_schema(conn)

    # Create edge schemas
    create_edge_schema(conn)


def create_import_files(
    path_parquet_data: str,
    path_organization_json: str,
    path_output: str,
):
    """
    Creates graph import files for KuzuDB

    Args:
        path_parquet_data (str): The path of to the parquet file containing the data.
        path_organization_json (str): The path of the JSON file containing the organization data.
        path_output (str): The path of the directory to store the import files.

    Returns:
        None
    """
    logging.info("Creating the import files for KuzuDB")

    # Read the parquet file
    logging.info("Reading the parquet file...")
    start = time.time()
    ocds_df = pd.read_parquet(path_parquet_data)
    end = time.time()
    logging.info(f"Time elapsed: {round(end - start, 2)} seconds")

    # Create the output directory if it doesn't exist
    if not os.path.exists(path_output):
        logging.info("Creating output directory")
        os.makedirs(path_output)

    # Create the output files
    logging.info("Creating output parquet files...")
    start = time.time()

    # 'Release' nodes
    logging.info("Creating nodes_releases.parquet...")
    release_cols = ["id", "ocid", "date", "initiationType", "language", "tedURL"]
    df = ocds_df[release_cols]
    df.loc[:, "date"] = pd.to_datetime(ocds_df["date"]).dt.date
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "nodes_releases.parquet"))

    # 'Organization' nodes
    logging.info("Creating nodes_organizations.parquet...")
    table = pa.json.read_json(path_organization_json)
    df = table.to_pandas()
    # Concatenate all the values in df['roles'] to a single string for now
    df["roles"] = df["roles"].apply(lambda x: " ".join(x))
    df["identifierNationalID"] = df["identifier"].apply(
        lambda x: x["id"] if pd.notnull(x) else ""
    )
    df["addressStreetAddress"] = df["address"].apply(
        lambda x: x["streetAddress"] if pd.notnull(x) else ""
    )
    df["addressLocality"] = df["address"].apply(
        lambda x: x["locality"] if pd.notnull(x) else ""
    )
    df["addressRegion"] = df["address"].apply(
        lambda x: x["region"] if pd.notnull(x) else ""
    )
    df["addressPostalCode"] = df["address"].apply(
        lambda x: x["postalCode"] if pd.notnull(x) else ""
    )
    df["addressCountryName"] = df["address"].apply(
        lambda x: x["countryName"] if pd.notnull(x) else ""
    )
    df["contactPointName"] = df["contactPoint"].apply(
        lambda x: x["name"] if pd.notnull(x) else ""
    )
    df["contactPointEmail"] = df["contactPoint"].apply(
        lambda x: x["email"] if pd.notnull(x) else ""
    )
    df["contactPointTelephone"] = df["contactPoint"].apply(
        lambda x: x["telephone"] if pd.notnull(x) else ""
    )
    df["contactPointFaxNumber"] = df["contactPoint"].apply(
        lambda x: x["faxNumber"] if pd.notnull(x) else ""
    )
    df["contactPointUrl"] = df["contactPoint"].apply(
        lambda x: x["url"] if pd.notnull(x) else ""
    )
    df["detailsUrl"] = df["details"].apply(lambda x: x["url"] if pd.notnull(x) else "")
    df = df.drop(
        columns=[
            "identifier",
            "additionalIdentifiers",
            "address",
            "contactPoint",
            "details",
        ]
    )
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(
        table,
        os.path.join(path_output, "nodes_organizations.parquet"),
    )

    # 'Tender' nodes
    logging.info("Creating nodes_tenders.parquet...")
    tender_cols = [
        "id",
        "title",
        "description",
        "status",
        "valueAmount",
        "valueAmountEur",
        "valueCurrency",
    ]
    df = pd.DataFrame(ocds_df["tender"].apply(lambda x: x if pd.notna(x) else None))
    df = pd.json_normalize(df["tender"].dropna(), max_level=0)
    df["valueAmount"] = df["value"].apply(
        lambda x: x["amount"] if pd.notna(x) else None
    )
    df["valueAmountEur"] = df["value"].apply(
        lambda x: x["amountEur"] if pd.notna(x) else None
    )
    df["valueCurrency"] = df["value"].apply(
        lambda x: x["currency"] if pd.notna(x) else None
    )
    table = pa.Table.from_pandas(df[tender_cols], preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "nodes_tenders.parquet"))

    # 'Award' nodes
    logging.info("Creating nodes_awards.parquet...")
    award_cols = ["id", "title", "status"]
    df = ocds_df.explode("awards", ignore_index=True)
    df = pd.json_normalize(df["awards"].dropna(), max_level=0)
    table = pa.Table.from_pandas(df[award_cols], preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "nodes_awards.parquet"))

    # 'Contract' nodes
    logging.info("Creating nodes_contracts.parquet...")
    contract_cols = [
        "id",
        "title",
        "status",
        "valueAmount",
        "valueAmountEur",
        "valueCurrency",
        "dateSigned",
    ]
    df = ocds_df.explode("contracts", ignore_index=True)
    df = pd.json_normalize(df["contracts"].dropna(), max_level=0)
    df["dateSigned"] = pd.to_datetime(df["dateSigned"]).dt.date
    df["valueAmount"] = df["value"].apply(
        lambda x: x["amount"] if pd.notna(x) else None
    )
    df["valueAmountEur"] = df["value"].apply(
        lambda x: x["amountEur"] if pd.notna(x) else None
    )
    df["valueCurrency"] = df["value"].apply(
        lambda x: x["currency"] if pd.notna(x) else None
    )
    table = pa.Table.from_pandas(df[contract_cols], preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "nodes_contracts.parquet"))

    # 'hasTender' edge (Release -> Tender)
    logging.info("Creating edges_hasTender.parquet...")
    release_ids = ocds_df["id"]
    tender_ids = ocds_df["tender"].apply(lambda x: x.get("id") if pd.notna(x) else None)
    df = pd.DataFrame({"from": release_ids, "to": tender_ids})
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "edges_hasTender.parquet"))

    # 'hasBuyer' edge (Release -> Organization)
    logging.info("Creating edges_hasBuyer.parquet...")
    buyer_ids = ocds_df["buyer"].apply(lambda x: x.get("id") if pd.notna(x) else None)
    df = pd.DataFrame({"from": release_ids, "to": buyer_ids})
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "edges_hasBuyer.parquet"))

    # 'hasAwards' edge (Release -> Award)
    logging.info("Creating edges_hasAwards.parquet...")
    df = ocds_df.explode("awards", ignore_index=True)
    df = df.dropna(subset=["awards"])
    df["from"] = df["id"]
    df["to"] = df["awards"].apply(lambda x: x["id"])
    df = df[["from", "to"]]
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "edges_hasAwards.parquet"))

    # 'hasContracts' edge (Award -> Contract)
    logging.info("Creating edges_hasContracts.parquet...")
    df = ocds_df.explode("contracts", ignore_index=True)
    df = df.dropna(subset=["contracts"])
    df["from"] = df["id"]
    df["to"] = df["contracts"].apply(lambda x: x["id"])
    df = df[["from", "to"]]
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "edges_hasContracts.parquet"))

    # 'hasSuppliers' edge (Award -> Organization)
    logging.info("Creating edges_hasSuppliers.parquet...")
    df = ocds_df.explode("awards", ignore_index=True)
    df = pd.json_normalize(df["awards"])
    df = df[["id", "suppliers"]]
    df = df.explode("suppliers", ignore_index=True)
    df = df.dropna(subset=["suppliers"])
    df["suppliers"] = df["suppliers"].apply(lambda x: x["id"])
    df = df.rename(columns={"id": "from", "suppliers": "to"}).reset_index(drop=True)
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, os.path.join(path_output, "edges_hasSuppliers.parquet"))

    end = time.time()
    logging.info(f"Time elapsed: {round(end - start, 2)} seconds")


def import_to_kuzu(path: str, conn: Connection):
    """
    Imports the data into KuzuDB

    Args:
        path (str): The path of the directory containing the import files.
        conn (Connection): The database connection object.

    Returns:
        None
    """
    # Start timer to track how long it takes to import data into KuzuDB
    logging.info("Importing data into KuzuDB...")
    start = time.time()

    # Import nodes
    logging.info("Importing Release nodes...")
    conn.execute(f"COPY Release FROM '{path}/nodes_releases.parquet'")
    logging.info("Importing organization nodes...")
    conn.execute(f"COPY Organization FROM '{path}/nodes_organizations.parquet'")
    logging.info("Importing Tender nodes...")
    conn.execute(f"COPY Tender FROM '{path}/nodes_tenders.parquet'")
    logging.info("Importing Award nodes...")
    conn.execute(f"COPY Award FROM '{path}/nodes_awards.parquet'")
    logging.info("Importing Contract nodes...")
    conn.execute(f"COPY Contract FROM '{path}/nodes_contracts.parquet'")

    # Import Edges
    logging.info("Importing edges...")
    conn.execute(f"COPY hasTender FROM '{path}/edges_hasTender.parquet'")
    conn.execute(f"COPY hasBuyer FROM '{path}/edges_hasBuyer.parquet'")
    conn.execute(f"COPY hasAwards FROM '{path}/edges_hasAwards.parquet'")
    conn.execute(f"COPY hasSuppliers FROM '{path}/edges_hasSuppliers.parquet'")
    conn.execute(f"COPY hasContracts FROM '{path}/edges_hasContracts.parquet'")
    conn.execute(f"COPY isSameAs FROM '{path}/edges_isSameAs.parquet'")

    # Stop timer
    end = time.time()
    logging.info(f"Time elapsed: {round(end - start, 2)} seconds")
    logging.info("Finished importing data into KuzuDB")
