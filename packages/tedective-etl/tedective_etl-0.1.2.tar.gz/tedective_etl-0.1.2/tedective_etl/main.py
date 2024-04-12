import argparse
import logging
import multiprocessing
import os
import shutil
import tarfile
from datetime import datetime
from urllib.request import urlretrieve

import luigi
import orjson
import orjsonl
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from kuzu import Connection, Database
from luigi import LocalTarget, Parameter, Task
from luigi.execution_summary import LuigiRunResult, LuigiStatusCode

from tedective_etl.currency.update import fetch_exchange_rates
from tedective_etl.dedupe import dedupe_organizations
from tedective_etl.graph import (create_import_files, create_kuzudb_schema,
                                 import_to_kuzu)
from tedective_etl.search import create_index
from tedective_etl.ted_to_ocds.process import (get_ted_xml_files,
                                               process_ted_notice)
from tedective_etl.ted_to_ocds.transform import implemented_forms
from tedective_etl.utils import prune_list


class DownloadCurrencyRates(Task):
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)
    output_dir = Parameter(default=None)

    def run(self):
        fetch_exchange_rates(self.first_month, self.last_month)

        with self.output().open("w") as f:
            f.write("Fetching exchange rates was completed successfully.")

    def output(self):
        return LocalTarget(os.path.join(self.output_dir, "download_currency_rates_complete.txt"))


class DownloadTEDNotices(Task):
    in_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)

    def run(self):
        os.makedirs(self.in_dir, exist_ok=True)
        #fetch_exchange_rates(self.first_month, self.last_month)

        start_date = datetime(
            int(self.first_month.split("-")[0]),
            int(self.first_month.split("-")[1]),
            1,
        )
        end_date = datetime(
            int(self.last_month.split("-")[0]),
            int(self.last_month.split("-")[1]),
            1,
        )

        for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
            year_month = dt.strftime("%Y-%m")
            if not os.path.isdir(f"{self.in_dir}/{year_month}"):
                if not os.path.isfile(f"{self.in_dir}/{year_month}.tar.gz"):
                    logging.info(f"Downloading TED XMLs for {year_month}...")
                    url = f"https://ted.europa.eu/packages/monthly/{year_month}"
                    dst = f"{self.in_dir}/{year_month}.tar.gz"
                    urlretrieve(url, dst)

                logging.info(f"Extracting TED XMLs for {year_month}...")
                f_to_extract = tarfile.open(f"{self.in_dir}/{year_month}.tar.gz")
                f_to_extract.extractall(f"{self.in_dir}/{year_month}")
                os.remove(f"{self.in_dir}/{year_month}.tar.gz")

                if year_month == self.last_month:
                    with open(
                        f"{self.in_dir}/{self.last_month}/complete.txt", "w"
                    ) as f:
                        f.write(
                            f"Download and extraction until {self.last_month} complete."
                        )

            else:
                logging.info(
                    f"Already downloaded and extracted TED XML for {year_month}."
                )

    def output(self):
        return LocalTarget(os.path.join(self.in_dir, self.last_month))


class ProcessTEDNotices(Task):
    in_dir = Parameter(default=None)
    output_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)

    def requires(self):
        return (
            DownloadTEDNotices(
                in_dir=self.in_dir,
                first_month=self.first_month,
                last_month=self.last_month,
            ),
            DownloadCurrencyRates(
                first_month=self.first_month,
                last_month=self.last_month,
                output_dir=self.output_dir,
            ),
        )

    def run(self):
        # Delete the output_dir if it exists
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        # Ensure the destination directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Get a list of the downloaded TED XML files
        ted_xml_files = get_ted_xml_files(
            in_dir=self.in_dir,
            first_month=self.first_month,
            last_month=self.last_month,
        )
        seen_org_ids = set()

        # Initialize counters for covered and uncovered XMLs
        num_uncovered = 0
        num_covered = 0

        # Set the previous month to the first_month parameter
        previous_month = self.first_month

        # Iterate over the XML files (they are grouped by day)
        for day, xml_files in ted_xml_files.items():
            # Get number of CPUs
            num_cpus = multiprocessing.cpu_count()
            # Process each XML file in parallel
            with multiprocessing.Pool(num_cpus - 4) as pool:
                results = pool.map(
                    process_ted_notice,
                    [(xml_file) for xml_file in xml_files],
                )

            # Initialize lists to store relevant data
            releases = []
            organizations = []

            # Split results into the appropriate lists
            for r in results:
                if r["form_type"] not in implemented_forms:
                    # Add to the number of uncovered XMLs
                    num_uncovered += 1
                else:
                    # Get the relevant data
                    releases += r["releases"]
                    organizations += r["organizations"]

                    # Add to the number of covered XMLs
                    num_covered += 1

            # Prune the organizations
            pruned_organizations = prune_list(organizations, seen_org_ids)
            seen_org_ids = pruned_organizations[1]

            # Write organizations to disk (append-only)
            with open(f"{self.output_dir}/organizations.jsonl", "a") as f:
                for o in pruned_organizations[0]:
                    f.write(
                        orjson.dumps(
                            o.model_dump(mode="json", exclude_none=False)
                        ).decode("utf-8")
                        + "\n"
                    )

            # Prune releases
            pruned_releases = list(set(releases))

            # Get the month as YYYY-MM
            month = day[:6]
            month = month[:4] + "-" + month[4:]

            # Write releases to disk (append-only)
            with open(f"{self.output_dir}/{month}_ocds_releases.json", "a") as f:
                for r in pruned_releases:
                    f.write(
                        orjson.dumps(
                            r.model_dump(mode="json", exclude_none=False)
                        ).decode("utf-8")
                        + "\n"
                    )

            # Calculate the coverage ratio
            coverage = num_covered / (num_covered + num_uncovered) * 100

            # This logs when the month changes, e.g. from 2017-01 to 2017-02
            if month != previous_month:
                logging.info(
                    f"Processed TED XMLs for {previous_month}. Overall coverage: {coverage:.2f}%"
                )
                previous_month = month

        # This logs only once at the end
        if month == self.last_month:
            logging.info(
                f"Processed TED XMLs for {self.last_month}. Overall coverage: {coverage:.2f}%"
            )
            previous_month = month

        # Create a dataframe to hold all the OCDS releases
        logging.info("Creating OCDS dataframe...")
        ocds_df = pd.DataFrame()

        # Transform the JSONL files to OCDS 1.1.5
        logging.info("Transforming JSON files to OCDS 1.1.5...")
        for filename in os.listdir(self.output_dir):
            if filename.endswith(".json") and not filename.startswith("organizations"):
                # Load the JSONL files
                filepath = os.path.join(self.output_dir, filename)
                data = orjsonl.load(filepath)
                # Only transform the OCDS releases, not the organizations
                # There will be one file for each month
                new_data = {
                    "version": "1.1.5",
                    "publishedDate": datetime.now(),
                    "releases": data,
                    "publisher": "TEDective Team",
                    "license": "ODbL-1.0",
                }
                # Append to dataframe
                tmp_df = pd.DataFrame(data)
                ocds_df = pd.concat([ocds_df, tmp_df])

                # Write to file
                with open(filepath, "w") as f:
                    f.write(orjson.dumps(new_data).decode("utf-8"))

        # Write ocds_df to parquet file
        logging.info("Write OCDS dataframe to parquet file")
        ocds_table = pa.Table.from_pandas(ocds_df, preserve_index=False)
        pq.write_table(ocds_table, os.path.join(self.output_dir, "ocds_data.parquet"))

    def output(self):
        return LocalTarget(
            os.path.join(self.output_dir, f"{self.last_month}_ocds_releases.json")
        )


class BuildSearchIndex(Task):
    meilisearch_url = Parameter(default=None)
    sleep_time = Parameter(default=3)
    in_dir = Parameter(default=None)
    output_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)

    def requires(self):
        return ProcessTEDNotices(
            in_dir=self.in_dir,
            output_dir=self.output_dir,
            first_month=self.first_month,
            last_month=self.last_month,
        )

    def run(self):
        # Create the search index
        create_index(
            meilisearch_url=self.meilisearch_url,
            output_path=self.output_dir,
            sleep_time=self.sleep_time,
        )
        # Write a file to indicate that the search index has been built
        with self.output().open("w") as f:
            f.write("Search index built successfully.")

    def output(self):
        return LocalTarget(os.path.join(self.output_dir, "search_index_complete.txt"))


class CreateKuzuDBImportFiles(Task):
    in_dir = Parameter(default=None)
    output_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)

    def requires(self):
        return ProcessTEDNotices(
            in_dir=self.in_dir,
            output_dir=self.output_dir,
            first_month=self.first_month,
            last_month=self.last_month,
        )

    def run(self):
        create_import_files(
            path_parquet_data=f"{self.output_dir}/ocds_data.parquet",
            path_organization_json=f"{self.output_dir}/organizations.jsonl",
            path_output=self.output_dir,
        )

    def output(self):
        return LocalTarget(os.path.join(self.output_dir, "edges_hasSuppliers.parquet"))


class DedupeOrganizations(Task):
    in_dir = Parameter(default=None)
    output_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)

    def requires(self):
        return ProcessTEDNotices(
            in_dir=self.in_dir,
            output_dir=self.output_dir,
            first_month=self.first_month,
            last_month=self.last_month,
        )

    def run(self):
        dedupe_organizations(
            path_organization_json=f"{self.output_dir}/organizations.jsonl",
            path_output=self.output_dir,
        )

    def output(self):
        return LocalTarget(os.path.join(self.output_dir, "edges_isSameAs.parquet"))


class LoadKuzuDB(Task):
    in_dir = Parameter(default=None)
    output_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)
    graph_dir = Parameter(default=None)

    def requires(self):
        return (
            ProcessTEDNotices(
                in_dir=self.in_dir,
                output_dir=self.output_dir,
                first_month=self.first_month,
                last_month=self.last_month,
            ),
            CreateKuzuDBImportFiles(
                in_dir=self.in_dir,
                output_dir=self.output_dir,
                first_month=self.first_month,
                last_month=self.last_month,
            ),
            DedupeOrganizations(
                in_dir=self.in_dir,
                output_dir=self.output_dir,
                first_month=self.first_month,
                last_month=self.last_month,
            ),
        )

    def run(self):
        # Remove graph at graph_dir if it already exists using shutil.rmtree
        if os.path.exists(self.graph_dir):
            shutil.rmtree(self.graph_dir)

        # Create the database and connection
        db = Database(self.graph_dir)
        conn = Connection(db)

        # Create the schema
        create_kuzudb_schema(conn)

        # Import the data
        import_to_kuzu(self.output_dir, conn)

        # Write a file to indicate that the data has been loaded
        with self.output().open("w") as f:
            f.write("Data loaded into KuzuDB successfully.")

    def output(self):
        return LocalTarget(os.path.join(self.output_dir, "load_kuzudb_complete.txt"))


class RunAllTasks(luigi.WrapperTask):
    """
    This class is a wrapper for the entire pipeline. It runs all the luigi tasks
    in the pipeline.
    """

    in_dir = Parameter(default=None)
    output_dir = Parameter(default=None)
    graph_dir = Parameter(default=None)
    first_month = Parameter(default=None)
    last_month = Parameter(default=None)
    meilisearch_url = Parameter(default=None)

    def requires(self):
        logging.info(f"Running all tasks with data until {self.last_month}...")
        try:
            # TODO Check if this is really needed
            if f"{self.last_month}_ocds_releases.json" not in os.listdir(
                self.output_dir
            ):
                shutil.rmtree(self.output_dir)
                shutil.rmtree(self.graph_dir)
                logging.warn(
                    f"Removed {self.graph_dir} and {self.output_dir} as all data needs to be reprocessed."
                )
        # If it's already gone for some reason, just don't error out
        except FileNotFoundError:
            pass

        return [
            # These are the tasks that no other task depends on
            BuildSearchIndex(
                meilisearch_url=self.meilisearch_url,
                in_dir=self.in_dir,
                output_dir=self.output_dir,
                first_month=self.first_month,
                last_month=self.last_month,
            ),
            LoadKuzuDB(
                graph_dir=self.graph_dir,
                in_dir=self.in_dir,
                output_dir=self.output_dir,
                first_month=self.first_month,
                last_month=self.last_month,
            ),
        ]


def run_pipeline() -> LuigiRunResult:
    """
    Run the TEDective ETL pipeline. This function serves as the entrypoint for
    running the entire pipeline via poetry scripts (defined in pyproject.toml).

    Args:
        first_month (str): The first month to process. Defaults to '2017-01'.
        last_month (str): The last month to process. Defaults to None.
        meilisearch_url (str): The URL of the Meilisearch server. Defaults to 'http://localhost:7700'.
        in_dir (str): The directory to store the TED XMLs. Defaults to '/tmp/ted_notices'.
        output_dir (str): The directory to store the output data. Defaults to '/tmp/output'.
        graph_dir (str): The name of the KuzuDB graph. Defaults to '/tmp/graph'.

    Returns:
        None
    """
    # HACK Provide all the args via the command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--first-month",
        help="The first month to process. Defaults to '2017-01'.",
        default="2017-01",
    )
    parser.add_argument(
        "--last-month",
        help="The last month to process. Defaults to the last month.",
        default=None,
    )
    parser.add_argument(
        "--meilisearch-url",
        help="The URL of the Meilisearch server. Defaults to 'http://localhost:7700'",
        default="http://localhost:7700",
    )
    parser.add_argument(
        "--in-dir",
        help="The directory to store the TED XMLs. Defaults to '/tmp/ted_notices'",
        default="/tmp/ted_notices",
    )
    parser.add_argument(
        "--output-dir",
        help="The directory to store the output data. Defaults to '/tmp/output'",
        default="/tmp/output",
    )
    parser.add_argument(
        "--graph-dir",
        help="The name of the KuzuDB graph. Defaults to '/tmp/graph'",
        default="/tmp/graph",
    )
    parser.add_argument(
        "--local-scheduler",
        help="Use the local scheduler.",
        action="store_true",
    )
    args = parser.parse_args()

    # If last_month is not provided, process TED XMLs until last complete
    # calendar month
    if args.last_month is None:
        logging.info("No end date provided. Processing TED XMLs until last month.")
        end_date = datetime.now() - relativedelta(months=1)
        args.last_month = end_date.strftime("%Y-%m")
    else:
        logging.info(f"Processing TED XMLs until {args.last_month}.")

    result = luigi.build(
        [
            RunAllTasks(
                first_month=str(args.first_month),
                last_month=str(args.last_month),
                meilisearch_url=str(args.meilisearch_url),
                in_dir=str(args.in_dir),
                output_dir=str(args.output_dir),
                graph_dir=str(args.graph_dir),
            ),
        ],
        detailed_summary=True,
        local_scheduler=args.local_scheduler,
    )
    if result.status == LuigiStatusCode.SUCCESS:
        logging.info("TEDective ETL pipeline completed successfully.")
        # Exit with status code 0
        exit(0)
    else:
        logging.error("TEDective ETL pipeline failed.")
        # Exit with status code 1
        exit(1)
