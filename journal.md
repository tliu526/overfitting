# Overfitting Journal and Notes

## 2019-05-28

### Lyle Meeting Notes

- need to make held out set be sampled from the same distribution as the training set
- if we want to use different distributions, have to show the differences in distributions
- papers: 
  - Andrew Ng's exponential features
  - Gellman (mathematician) forest of branching paths, Bonferroni corrections
- Lyle's hypothesis for classification:
  - all models will have most of the mass near 0 or 1 on the training data
  - properly fit models will have a similar distribution
  - over fit models will have much of their mass near 0.5, assuming a balanced training set
- Lyle's hypothesis for regression:
  - probability distribution with y-hat on x axis, $p(\hat{y})$ on the y
  - $\hat{y}_{train}$ will have the same density as the true distribution
  - $\hat{y}_{test}$ will have a different distribution, shrunk closer to the training mean
- slight complication:  
  - linear regression is shrunk when correct
  - "noise" is equivalent to missing information

- potential "games" to play:
  - given the model (w-hats), and training error ($|y_t - \hat{y}_t|_2$), can we determine whether or not the model is overfit?
  - permutation test with unlabelled X's of a paper's algorithmic procedure to test for overfitting

- simplest case to model:
  - all noise, no connection between labels and X's
  - as the number of features increases we should see the density of the probability converge to the training distribution of labels (eg 50/50), with greater "peakiness" (central limit theorem) as the number of features asymptotes to infinitys
- potential connections with permutation tests
