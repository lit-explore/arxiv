# arXiv Data Preparation Pipeline

## Overview

This repo contains a [Snakemake](https://snakemake.readthedocs.io/) pipeline for downloading and
processing [arXiv](https://arxiv.org/) article data into a format that can be easily used by other
efforts.

Article data is retrieve via the [Kaggle arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv), which is updated weekly, and at
the time of writing, includes ~1.7m articles.

To retrieve the data, the [kaggle CLI](https://github.com/Kaggle/kaggle-api) is used to query the Kaggle API.

To do so, one much first create and account and authenticate it, as described [in the kaggle API
docs](https://github.com/Kaggle/kaggle-api#api-credentials).

These files are then parsed, and the following fields are extracted for each article:

1. ID
2. DOI
3. Title
4. Abstract
5. Date

The "ID" field in this case refers to the the article's arXive ID. In some cases, one or more of
the fields may be missing, and the pipeline can be configured to optionally exclude articles which
are missing either/both title and abstract information.

For each article, tokenization and lemmatization is performed and the results are stored separately,
so that for each article, two alternate versions of the article text are created.

In order to support parallization in downstream steps, articles are stored in batches with a
configurable size.

For more information about the source data, see: [arXiv Dataset | Kaggle](https://www.kaggle.com/datasets/Cornell-University/arxiv)

## Usage

To use the pipeline, first create and activate a [conda
environment](https://docs.conda.io/en/latest/) using the provided `requirements.txt` file:

```
conda create -n arxiv --file requirements.txt
conda activate arxiv
```

Next, copy the example config file, `config/config.example.yml`, and modify the config to indicate
the desired output directory to use, along with any other changes to the settings.

```
cp config/config.example.yml config/config.yml
```

Finally, launch the Snakemake pipeline, provided the config file along with any other desired
settings, e.g.:

```
snakemake -j4 --configfile config/config.yml
```

## Related

For a similar pipeline for retrieving and processing PubMed data, see: [lit-explore/pubmed](https://github.com/lit-explore/pubmed).
