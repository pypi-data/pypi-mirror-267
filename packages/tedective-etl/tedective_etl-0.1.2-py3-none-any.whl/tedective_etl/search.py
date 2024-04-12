import logging
import os
import time

import orjson
from meilisearch import Client


def create_index(
    meilisearch_url: str = "http://localhost:7700",
    output_path: str = "/tmp/output",
    sleep_time: int = 7,
):
    # Create a Meilisearch client
    client = Client(meilisearch_url)

    # Delete indexes if they exist
    try:
        client.delete_index("organizations")
        client.delete_index("awards")
        client.delete_index("contracts")
    except Exception as e:
        logging.error(f"Error deleting indexes: {e}")

    logging.info("Existing indexes deleted")

    # Load file located at ../tedective-parser/output/organizations.jsonl into string
    # and then load the string into a list of dictionaries
    with open(os.path.join(output_path, "organizations.jsonl"), "r") as f:
        logging.info("Loading 'organizations' list into memory...")
        organizations = [orjson.loads(line) for line in f.readlines()]

    # Add documents to index
    logging.info("Adding 'organizations' to index...")
    index = client.index("organizations")
    index.update_filterable_attributes(
        [
            "address.locality",
            "address.region",
            "address.countryName",
            "roles",
            "details.classifications.id",
        ]
    )
    # Log size in MB of organizations list
    logging.debug(
        f"Size of 'organizations' list: {round(len(orjson.dumps(organizations)) / 1024 / 1024, 2)} MB"
    )
    # Chunk the list of organizations into smaller lists of 100000 items
    # and add each chunk to the index
    CHUNK_SIZE = 100000  # Make this a constant or a parameter
    for i in range(0, len(organizations), CHUNK_SIZE):
        try:
            index.add_documents(organizations[i : i + CHUNK_SIZE])
            logging.info(
                f"Chunk {(i // CHUNK_SIZE) + 1} from 'organizations' added to index tasks"
            )
            logging.info(
                f"Sleeping for {str(sleep_time)}s to give meilisearch some time to index..."
            )
            time.sleep(sleep_time)
        except Exception as e:
            logging.error(
                f"Failed to add 'organizations' chunk {i // CHUNK_SIZE} to index tasks: {e}"
            )

    # Load files located at ../tedective-parser/output/YYYYMM_ocds_releases.json into string
    for file in os.listdir(output_path):
        awards = []
        contracts = []
        if file.endswith(".json"):
            with open(os.path.join(output_path, file), "r") as f:
                # This is one big dictionary with a list of relevant
                # dictionaries under the key "releases"
                ocds = orjson.loads(f.read())

                # Get the list of releases
                releases = ocds["releases"]
                logging.debug(f"'{file}' loaded into memory")

                # Get the list of awards from each release
                for release in releases:
                    if release["awards"]:
                        for award in release["awards"]:
                            award = {k: v for k, v in award.items() if v}
                            awards.append(award)
                    if release["contracts"]:
                        for contract in release["contracts"]:
                            contract = {k: v for k, v in contract.items() if v}
                            contracts.append(contract)

                # Add awards to index
                index = client.index("awards")
                index.update_filterable_attributes(["status"])
                index.add_documents(awards, primary_key="id")
                logging.info(f"Awards from '{file}' added to 'awards' index")
                logging.info(
                    f"Sleeping for {str(sleep_time)}s to give meilisearch some time to index..."
                )
                time.sleep(sleep_time)

                # Add contracts to index
                index = client.index("contracts")
                index.update_filterable_attributes(["status", "value.currency"])
                index.update_sortable_attributes(["dateSigned", "value.amount"])
                index.add_documents(contracts, primary_key="id")
                logging.info(f"Contracts from '{file}' added to 'contracts' index")
                logging.info(
                    f"Sleeping for {str(sleep_time)}s to give meilisearch some time to index..."
                )
                time.sleep(sleep_time)
