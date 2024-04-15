# ETL

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![REUSE status](https://api.reuse.software/badge/git.fsfe.org/TEDective/etl)](https://api.reuse.software/info/git.fsfe.org/TEDective/etl)

The code in this repo is part of the TEDective project. It defines an ETL
pipeline to transform European public procurement data from Tenders Electronic
Daily (TED) into a format that's easier to handle and analyse. Primarily, the
TED XMLs (and eForms, WIP) are transformed into Open Contracting Data
Standard (OCDS) JSON and parquet files to ease importing the data into a:

- Graph database (KuzuDB in our case, but processed data should be generic
  enough to support any graph database and a
- Search engine (Meilisearch in our case)

Organizations are deduplicated using Splinkg and linked to their GLEIF
identifiers (WIP) before they are imported into the graph database.

## Table of Contents for ETL

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

The TEDective project aims to make European public procurement data explorable
for non-experts. This transformation is more or lest based on the [Open
Contracting Data Standard (OCDS) EU
Profile](https://standard.open-contracting.org/profiles/eu/latest/en/):

As such, this pipeline can be used standalone or as part of your project that
does something interesting with TED data. We use it ourselves for the
[TEDective API](https://git.fsfe.org/TEDective/api) that powers the [TEDective
UI](https://git.fsfe.org/TEDective/ui).

## Install

:construction: Disclaimer: install instructions are working as of 12th of April 2024, but they may be subject of change.

The ETL consist of two parts the pipeline and the Luigi server (scheduler)

### Using PyPi package

The easiest way to install TEDective ETL is to use PyPi package via `pipx`:
```bash
pipx install tedective-etl
pipx ensurepath # to make sure it has been added to your path
run-pipeline --help
```

### Using Nix:
```bash
# Install flake into your profile
nix profile install git+https://git.fsfe.org/TEDective/etl
run-pipeline --help
```

Alternatively, you can clone this repository and build it via Nix yourself 

```bash
# Cloning the repository and entering it
git clone https://git.fsfe.org/TEDective/etl && cd etl

# Nix build using the provided flake
nix build

# Disclaimer nix-commands and flakes are experimental features so you will need to add these flags to the command to be able to run them.
--extra-experimental-features 'nix-command flakes'
# You will also been prompted to accept/decline some extra configurations. You can accept them without receiving a prompt using this or manually decide without adding it:
--accept-flake-config
```

### Manually
Another way is to use `poetry` directly.

After cloning this repo:

```bash
poetry install
poetry run run-pipeline --help
```

## Usage

:construction: Disclaimer: usage instructions are working as of 12th of April 2024, but they may be subject of change.

### Genaral usage options
```bash
run-pipeline [-h] [--first-month FIRST_MONTH] [--last-month LAST_MONTH]
                    [--meilisearch-url MEILISEARCH_URL] [--in-dir IN_DIR]
                    [--output-dir OUTPUT_DIR] [--graph-dir GRAPH_DIR] [--local-scheduler]

options:
  -h, --help            show this help message and exit
  --first-month FIRST_MONTH
                        The first month to process. Defaults to '2017-01'.
  --last-month LAST_MONTH
                        The last month to process. Defaults to the last month.
  --meilisearch-url MEILISEARCH_URL
                        The URL of the Meilisearch server. Defaults to
                        'http://localhost:7700'
  --in-dir IN_DIR       The directory to store the TED XMLs. Defaults to '/tmp/ted_notices'
  --output-dir OUTPUT_DIR
                        The directory to store the output data. Defaults to '/tmp/output'
  --graph-dir GRAPH_DIR
                        The name of the KuzuDB graph. Defaults to '/tmp/graph'
  --local-scheduler     Use the local scheduler.
```

### Using PyPi package
After installation you should able to run both Luigi scheduler and pipeline:
```bash
run-server
# In different window
run-pipeline
```
Another extra thing that can be ran is a Meilisearch instance so that the search indexes can be built is `meilisearch`.
It is *NOT* provided together with PyPi package, you can install it using your favourite package manager. It is recommended to install it if you plan to use the parsed data with [TEDective API](https://git.fsfe.org/TEDective/api)

### Using Nix
```bash
# The nix build will create a result folder inside it you will find these scripts
# This is how you can get more information about the possible arguments you can provide to the script
result/bin/run-pipeline --help

# IMPORTANT: As we previously said there are two parts to the ETL this is how to spin up luigi so the pipeline can run
result/bin/run-server

# We suggest for development purposes to use the --last-month flag to have it quickly setup. You can also set the first-month if you would like a specific time window of data. By default first month is going to be 2017-01
run-pipeline --last-month 2017-02
```
In this case you can also run Meilisearch to build search indexes. That can be done inside the devenv more on that further [down](#contributing)


### Manually (using `poetry`)
Running the pipeline requires running luigi daemon. It is included in the
project and you can run it with the following command:

```bash
poetry run run-server
# And pipeline itself in different window
poetry run run-pipeline
```

It is recommended to run Meilisearch as well, if using this method, you would have to install it manually as well.

## Maintainers

[@linozen](https://github.com/linozen)<br/>
[@micgor32](https://github.com/micgor32)

## Contributing

##### 1. Nix development environment 

The easiest way to start developing if you are using nix is to use [devenv](https://devenv.sh) via
the provided `flake.nix`.

```bash
# If you have Nix installed
nix develop --impure
# This will drop you into a shell with all the dependencies installed
# And it will also require the experimental flags:
# Disclaimer nix-commands and flakes are experimental features so you will need to add these flags to the command to be able to run them.
--extra-experimental-features 'nix-command flakes'
# You will also been prompted to accept/decline some extra configurations. You can accept them without receiving a prompt using this or manually decide without adding it:
--accept-flake-config

# Inside you have all the needed tools

# These will provide you with the amazing kuzu-explorer which allows you to run queries to the database.
kuzu-up
# And
kuzu-down

# Inside the devenv you also have access to Mielisearch

# Inside the devenv pre-commits are setup with all other checks so that is the easiest way to make a commit to the repo.
```

##### 2. Editing documentation

Small note: If editing the README, please conform to the
[standard-readme](https://github.com/RichardLitt/standard-readme)
specification. Also, please ensure that documentation is kept in sync with the
code. Please note that the main documentation repository is added to this
repository via [git-subrepo](https://github.com/ingydotnet/git-subrepo). To
update the documentation, please use the following commands:

```bash
git-subrepo pull docs
cd ./docs

# Make your changes
git commit -am "docs: update documentation for new feature"

# Preview your changes
pnpm install
pnpm run dev

# If you're happy with your changes, push them
git-subrepo push docs
```

## License

EUPL-1.2 © 2024 Free Software Foundation Europe e.V.
