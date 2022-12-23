"""
lit-explore: arXiv Data Preparation
"""
import os
from os.path import join

configfile: "config/config.yml"

# arxiv article subset ids
arxiv_num = [f"{n:04}" for n in range(1, config['num_chunks'] + 1)]

rule all:
    input:
        join(config["out_dir"], "corpus/raw.feather"),
        join(config["out_dir"], "corpus/lemmatized.feather")

rule combine_arxiv_articles:
    input:
        expand(join(config["out_dir"], "raw/{arxiv_num}.feather"), arxiv_num=arxiv_num)
    output:
        join(config["out_dir"], "corpus/raw.feather")
    script:
        "scripts/combine_articles.py"

rule combine_arxiv_lemmatized_articles:
    input:
        expand(join(config["out_dir"], "lemmatized/{arxiv_num}.feather"), arxiv_num=arxiv_num)
    output:
        join(config["out_dir"], "corpus/lemmatized.feather")
    script:
        "scripts/combine_articles.py"


rule create_lemmatized_arxiv_corpus:
    input:
        join(config["out_dir"], "raw/{arxiv_num}.feather")
    output:
        join(config["out_dir"], "lemmatized/{arxiv_num}.feather")
    script:
        "scripts/lemmatize_text.py"

rule parse_arxiv_json:
    input:
        join(config["out_dir"], "json/arxiv-metadata-oai-snapshot.json")
    output:
        join(config["out_dir"], "raw/{arxiv_num}.feather")
    script:
        "scripts/parse_arxiv_json.py"

rule download_arxiv_data: 
    output:
        join(config["out_dir"], "json/arxiv-metadata-oai-snapshot.json")
    shell:
        """
        cd `dirname {output}`
        kaggle datasets download -d "Cornell-University/arxiv"
        unzip arxiv.zip
        rm arxiv.zip
        """

# vi:syntax=snakemake
