# etl

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![REUSE status](https://api.reuse.software/badge/git.fsfe.org/TEDective/etl)](https://api.reuse.software/info/git.fsfe.org/TEDective/etl)

The code in this repo is part of the TEDective project. It defines an ETL
pipeline to transform European public procurement data from Tenders Electronic
Daily (TED) into a format that's easier to handle and analyse. Primarily, the
TED XMLs (and eForms, WIP) are transformed into Open Contracting Data
Standard (OCDS) JSON and parquet files to ease importing the data into a:

- Graph database (KuzuDB in our case, but processed dataa should be generic
  enough to support any graph database and a
- Search engine (Meilisearch in our case)

Organizations are deduplicated using Splinkg and linked to their GLEIF
identifiers (WIP) before they are imported into the graph database.

## Table of Contents

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

The easiest way to install TEDective ETL is to use PyPi package:

```bash
pip install tedective-etl
run-pipeline --help
```

You can also install it via Nix:

```bash
# Install flake iinto your profile
nix profile install git+https://git.fsfe.org/TEDective/etl
run-pipeline --help
```

Alternatively, you can clone this repository and build it via Nix yourself:

```bash
git clone https://git.fsfe.org/TEDective/etl
cd etl
nix-build
result/bin/run-pipeline --help
```

Another way is to use `poetry` directly:

```bash
poetry install
poetry run run-pipeline --help
```

Running the pipeline requires running luigi daemon. It is included in the
project and you can run it with the following command:

```bash
# If using pip
run-server
# If using Nix
result/bin/run-server
# If using poetry
poetry run run-server
```

## Usage

:construction: This is still under heavy development.

## Maintainers

[@linozen](https://github.com/linozen)
[@micgor32](https://github.com/micgor32)

## Contributing

The easiest way to start developing is to use [devenv](https://devenv.sh) via
the provided `flake.nix`. So, clone this repository and run:

```bash
# If you have Nix installed
nix develop --impure
# This will drop you into a shell with all the dependencies installed
# If you want to bring up a meilisearch instance, simply run:
devenv up
```

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
