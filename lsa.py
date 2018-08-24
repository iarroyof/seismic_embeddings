"""Pirated example from Gensim library (a NLP specialized tool):
https://radimrehurek.com/gensim/tut2.html
https://radimrehurek.com/gensim/wiki.html#latent-semantic-analysis

Ignacio Arroyo
"""

import gensim
import logging
from six import iteritems
from gensim import corpora
from gensim.utils import tokenize
import argparse
import codecs


class corpus_streamer(object):
    """ This Object streams the input raw text file row by row.
    """
    def __init__(self, file_name, dictionary=None, strings=None, tokenizer=True):
        self.file_name=file_name
        self.dictionary=dictionary
        self.strings=strings
        self.tokenizer=tokenizer

    def __iter__(self):
        for line in codecs.open(self.file_name, 'r', 'latin-1'):#open(self.file_name):
        # assume there's one document per line, tokens separated by whitespace
            if self.dictionary and not self.strings:
                yield self.dictionary.doc2bow(line.lower().split())
            elif not self.dictionary and self.strings:
                if not self.tokenizer:
                    #yield u"".join(cl(line)).strip().lower()
                    yield line.strip().lower()
                if self.tokenizer:
                    #yield list(tokenize(u" ".join(cl(line))))
                    yield line.split() #codecs.open(vector_file, 'r', 'latin-1')
# Logging all our program
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

parser = argparse.ArgumentParser(description='LSA processing of a linguistically built dataset of Gensor Units.')
parser.add_argument("--n_topics", help="Number of eigenvectors picked up.",
                    default=2, type=int)
parser.add_argument("--doc_tags", help="The desired tags for each input document. First document word is taken if not provided",
                    default=None)
parser.add_argument("--input", help="Input file to perform LSA.",
                    required=True)
parser.add_argument("--stop",
              action="store_true", default=False, help="Toggles use of stop words.")
parser.add_argument("--tok",
              action="store_true", default=False, help="Toggles use of tokenizer without punctuation and numbers.")

args = parser.parse_args()

n_topics=args.n_topics
n_docs=0
input_file=args.input
#input_file='/medargsia/iarroyof/Volumen de 384 GB/data/GUs_textform_noPeriods.txt'
#input_file='lsa_example.csv'
#input_file='wiki_sample/wiki_75_AA.txt.cln'
#input_file='wiki_sample/wiki_77_AA.txt'

# A little stopwords list
if args.stop:
    stoplist = map(str.strip, open("stop_words.txt").readlines())
else:
    stoplist = set('for a of the and to in _ [ ]'.split())
# Do not load the text corpus into memory, but stream it!
fille=corpus_streamer(input_file, strings=True, tokenizer=args.tok)

dictionary=corpora.Dictionary(line for line in fille)#open(input_file))
# remove stop words and words that appear only once
stop_ids=[dictionary.token2id[stopword] for stopword in stoplist
                                             if stopword in dictionary.token2id]
once_ids=[tokenid for tokenid, docfreq in iteritems(dictionary.dfs)
                                                            if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)
# remove gaps in id sequence after words that were removed
dictionary.compactify()
# Store the dictionary
dictionary.save('lsa_mini.dict')
# Reading sentences from file into a list of strings.
# Use instead streaming objects:
# Load stored word-id map (dictionary)
stream_it = corpus_streamer(input_file, dictionary=dictionary, tokenizer=args.tok)
#for vector in stream_it:  # load one vector into memory at a time
#    print vector
# Convert to sparse matrix
sparse_corpus = [text for text in stream_it]
# Store to disk, for later use collect statistics about all tokens
corpora.MmCorpus.serialize('lsa_mini.mm',
                            sparse_corpus)
## LSA zone
# load the dictionary saved before
id2word = dictionary.load('lsa_mini.dict')
# Now load the sparse matrix corpus from file into a (memory friendly) streaming
# object.
corpus=corpora.MmCorpus('lsa_mini.mm')

## IF TfidfModel
tfidf = gensim.models.TfidfModel(corpus) # step 1 -- initialize a model
corpus = tfidf[corpus]
## FI TfidfModel
# Compute the LSA vectors
lsa=gensim.models.lsimodel.LsiModel(corpus, id2word=dictionary,
                                                     num_topics=n_topics)#, chunksize=1, distributed=True)
#st()
# Print the n topics in our corpus:
#lsa.print_topics(n_topics)
f=open("topics_file.txt","w")
N=lsa.num_topics

for t in range(N):
    f.write("%s\n" % lsa.show_topic(t, topn=n_topics))
f.close()

# create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
corpus_lsa = lsa[corpus]
# Stream sentences from file into a list of strings called "sentences"
sentences=corpus_streamer(input_file, strings=True, tokenizer=False)
n=0
if args.doc_tags is None:
    for pertenence, sentence in zip(corpus_lsa, sentences):
        if n_docs <= 0:
        #print "%s\t\t%s" % (pertenence, sentence.split("\t")[0])
            p=[dict(pertenence)[x] if x in dict(pertenence) else 0.0
                                            for x in range(n_topics)]
            print ("%s %s" % ("".join(sentence.split("\t")[0].split()),
                            "".join(str(p)[1:].strip("]").split(",")) ))
        else:
            if n<n_docs:
                pertenence=[dict(pertenence)[x] if x in dict(pertenence) else 0.0
                                                    for x in range(n_topics)]
                print ("%s\t\t%s" % (pertenence, sentence))
                n+=1
            else:
                break
else:
    #with open(args.doc_tags) as f:
    with codecs.open(args.doc_tags, 'r', 'latin-1') as f:
        tags=f.readlines()

    for pertenence, tag in zip(corpus_lsa, tags):
        if n_docs <= 0:
            p=[dict(pertenence)[x] if x in dict(pertenence) else 0.0
                                            for x in range(n_topics)]
            print ("%s %s" % (tag.strip(), "".join(str(p)[1:].strip("]").split(",")) ))
        else:
            if n<n_docs:
                pertenence=[dict(pertenence)[x] if x in dict(pertenence) else 0.0
                                                    for x in range(n_topics)]
                print ("%s\t\t%s" % (tag.strip(), pertenence))
                n+=1
            else:
                break

