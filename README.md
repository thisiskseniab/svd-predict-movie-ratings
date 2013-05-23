Kwickster
=========================
http://ksenish.github.io/svd-predict-movie-ratings

Overview
========
My Hackbright project - Kwickster! 

Movie recommendation engine (rating prediction algorithm) based on Singular Value Decomposition

Data from MovieLens (10M100K) - http://ksenish.github.io/svd-predict-movie-ratings/data.html


Algorithm
=========
Code - https://github.com/ksenish/svd-predict-movie-ratings/blob/master/bin/svd.py
About - http://ksenish.github.io/svd-predict-movie-ratings/svd_page.html

The whole data is presented as a sparse matrix (10 million of original ratings).
The result of SVD training are the feature vectors, the sums of products of which for
each appropriate cell result in an accurate predictions. 
The first set of vectors is trained on the original data, the second on the error matrix, etc.
As a result, feature vectors take into account everything that can have effect on user's predictions: 
favorite genres, actors, directors, etc. Because of the way they are computed, the first feature is 
the 'heaviest' - takes into account everything that has the most effect on user's rating.

Formulas to compute the error and training of each vectors:

(*) error = (A' - Aa) * lrate

Error is the difference between the original rating (A') and product of vectors (Aa), times learning 
rate (lrate). Learning rate is a very small number that normalizes vectors during the training. 

(*)uF[u] += error * mF[m] 

For each user in a user vector add the value of itself and the product of the error and the appropriate 
value in the movie vector for each movie

(*)mF[m] += error * uF[u]

For each movie in a movie vector add the value of itself and the product of the error and the appropriate 
value in the user vector for each user

Memory Consumption
==================
In the naive implementation, the original ratings data represented as a matrix takes up 3.5GB or RAM.
Because the training is done on the whole matrix, for each vector 2 additional matrices are set up - 
Prediction Matrix and the Error Matrix. Each one of them is the same size, which means that every time
the new feature is trained the memory consumption increases by 7GB. 

This is inefficient. So instead of setting up 2 additional matrices for each feature, I use Lazy 
Evaluation to look up the value on the spot, do the computations with it, without holding the whole
matrix in memory.

About - http://ksenish.github.io/svd-predict-movie-ratings/lazy-eval.html

Speed Concerns
==============
The full training of 5 feature vectors with 800 ipf(iterations per features) takes 3.5 days even after 
implementing Lazy Evaluation.

Python is inefficient in looping over the whole data of almost 70,000 users and 11,000 users, and this
loop in training of each feature takes the longest - https://github.com/ksenish/svd-predict-movie-ratings/blob/master/bin/svd.py#L140-L152

Future Optimization Techniques
==============================
(*) Map Reduce/Hadoop 

Because of the way math is computed in SVD, I wasn't able to break up the code so computations could be done idempotent of each other. However, there is a possibility it might be done.

(*) Multithreading

The same concerns as with previous technique. It is possible that the problematic loop can be broken down in several parts and computed separately, but I wasn't able to figure out the way yet. 





