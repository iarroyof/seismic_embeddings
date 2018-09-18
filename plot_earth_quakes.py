# Version pirated from
# https://medium.com/@aneesha/using-tsne-to-plot-a-subset-of-similar-words-from-word2vec-bb8eeaea6229

import gensim
# Need the interactive Tools for Matplotlib
#%matplotlib notebook
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from matplotlib import rc

rc('text', usetex=True)
from pdb import set_trace as st


k = 15
d = "20"
q = '2017-09-19' #13h'
#q = "1985-09-19" #07h"
#embed_name = ("seismic_LSAembeddings_%s.vec" % d, False)
embed_name = ("word2vec_%sd_w3.bin" % d, True)


def display_closest_earthquakes(model, word):

    dim = model[q].shape[0]
    arr = np.empty((0,dim), dtype='f')
    word_labels = [word]

    # get close words
    close_words = model.similar_by_word(word, topn=k)

    # add the vector for each of the closest words to the array
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)

    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)

    bold = True
    for label, x, y in zip(word_labels, x_coords, y_coords):
        if bold:
            blabel = r"\textbf{%s}" % label
        else:
            blabel = label
        plt.annotate(blabel, xy=(x, y), xytext=(0, 0), textcoords='offset points', weight=bold)
        bold = False
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    return plt

# load pre-trained word2vec embeddings
# The embeddings can be downloaded from command prompt:

model = gensim.models.KeyedVectors.load_word2vec_format(
              			embed_name[0], binary=embed_name[1])


display_closest_earthquakes(model, q)

plt.show()
