# seismic_embeddings
This project aims to represent seismic data samples in an embedding space to observe similarities among embeddings. Data samples were provided by the Mexican National Seismic service (Servicio Sismológico Nacional) including intensity measurements from 1900 to 2018.

# Plotting seismic embeddings 2D projections
In order to represent earthquakes we used two different approaches. First, I embedded each object present in the input file by using Word2Vec algorithm. This creates a vector representation for each these objects suah as earthquake intesities and dates. The second approach was Latent Semantic Analysis, which is not showed in this README (the plots can be seen ![here 1985](https://github.com/iarroyof/seismic_embeddings/blob/master/figures/19S1985_LSA_20d.pdf) and ![here 2017](https://github.com/iarroyof/seismic_embeddings/blob/master/figures/19S2017_LSA_20d.pdf))

In this picture you can be the 15 nearest neighbors of the earthquake occurred in September 19th (2017), where representations used were Word2Vec. The points show vector representations projected into a 2D TSNE embedding for visualization:

![](https://github.com/iarroyof/seismic_embeddings/blob/master/figures/19S2017_W2V_20d.png)

In next picture you can be the 15 nearest neighbors of the earthquake occurred in September 19th (1985), where representations used were also Word2Vec.

![](https://github.com/iarroyof/seismic_embeddings/blob/master/figures/19S1985_W2V_20d.png)

We are not experts in seismic science, however, data show that in both cases (1985 and 2017) there are related poits. For example, in the pictures, look for a number of hearthquakes occurred in April 2017 which are considered to be in the context of those occured in September. Similarly, there are a number of hearthquakes occurred during September, near to the main one ocurred in 19S 2017.

It is pendding to observe in detail what makes those hearthquakes similar.
