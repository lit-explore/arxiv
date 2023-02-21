"""
Generates lemmatized version of a corpus
"""
import stanza
import pandas as pd

# pos batch size
POS_BATCH_SIZE = 501

snek = snakemake

# initialize stanza lemmatizer
nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma', 
                      pos_batch_size=POS_BATCH_SIZE)

# load corpus
corpus = pd.read_feather(snek.input[0])

corpus.abstract.fillna("", inplace=True)
corpus.title.fillna("", inplace=True)

# lists to store output row parts
ids:list[str] = []
dois:list[str] = []
lemma_titles:list[str] = []
lemma_abstracts:list[str] = []

docs:list[str] = []

for _, article in corpus.iterrows():
    ids.append(article.id)
    dois.append(article.doi)

    # collapse title and abstract for faster processing
    text = article.title.lower() + "\n\n" + article.abstract.lower()

    docs.append(text)

lemma_docs: list[str] = []

# lemmatize texts
out_docs = nlp([stanza.Document([], text=d) for d in docs])

# extract lemmatized titles and abstracts
for doc in out_docs:
    # extract title
    title_words:list[str] = [word.lemma for word in doc.sentences[0].words if word.lemma is not None]
    lemma_titles.append(" ".join(title_words))

    # extract abstract
    abstract_words:list[str] = []

    for sentence in doc.sentences[1:]:
        for word in sentence.words:
            if word.lemma is not None:
                abstract_words.append(word.lemma)

    abstract:str = " ".join(abstract_words).replace(" .", ".")

    lemma_abstracts.append(abstract)

df = pd.DataFrame({
    "id": ids,
    "doi": dois,
    "title": lemma_titles,
    "abstract": lemma_abstracts
})

df.to_feather(snek.output[0])
