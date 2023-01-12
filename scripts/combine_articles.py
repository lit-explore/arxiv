"""
Create a single file containing all article texts;
simplifies downstream processing.
"""
import pandas as pd

snek = snakemake

combined = pd.read_feather(snek.input[0])

num_batches = len(snek.input)

# iterate over batches of articles
for i, infile in enumerate(snek.input[1:]):
    if (i % 100 == 0) and i != 0:
        print(f"Processing article batch {i}/{num_batches}...")

    # append article batch to growing dataframe
    df = pd.read_feather(infile)
    combined = pd.concat([combined, df])

combined = combined.reset_index(drop=True)
combined.to_feather(snek.output[0])
