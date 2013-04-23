Traceback (most recent call last):
  File "app_main.py", line 52, in run_toplevel
  File "svd_2.py", line 367, in <module>
    uFs, mFs = train_some_features(test_matrix, 10)
  File "svd_2.py", line 345, in train_some_features
    uF, uM = train_one_feature_our_way(remainder, sigma)
  File "svd_2.py", line 328, in train_one_feature_our_way
    error = abs(lrate * (predicted.index(w, h) - predict_rating(real, h, w)))
  File "svd_2.py", line 213, in predict_rating
    average_user_off = average_user_offset(ratings, user)
  File "svd_2.py", line 194, in average_user_offset
    count_user = count_of_user_ratings(ratings, user)
  File "svd_2.py", line 166, in count_of_user_ratings
    r = ratings.index(user, x)
  File "svd_2.py", line 23, in index
    return self.matrix[w][h]
IndexError: wrong index

real	0m0.383s
user	0m0.079s
sys	0m0.056s
