
import numpy as np
import random
from scipy import stats
from sklearn import linear_model
n = 5 # number of features
N = 100 # number of observations
np.set_printoptions(precision=4)

covariance = np.zeros((n,n))
for i in xrange(n):
  for j in xrange(n):
    covariance[i,j] = covariance[j, i] if covariance[j, i] != 0 else 2*random.random()-1
covariance = covariance.dot(np.matrix.transpose(covariance))
#

print "covariance:\n{cov}\n".format(cov=covariance)

outliers = random.sample(range(N), 5)

print "outliers:\n{cov}\n".format(cov=outliers)

outlier_mean = np.random.randint(1,10, size=n)

print "outlier_mean:\n{cov}\n".format(cov=outlier_mean)

def random_vector_with_outliers(R, N=1):
  k = len(R[0]) # = n
  mean = np.random.uniform(-5,5, size=k)
  x = map(lambda i: mean + np.linalg.cholesky(R).dot(np.random.normal(size=k)), xrange(N))
  for (i, index) in enumerate(outliers):
    if i in [0, 1]:
      x[index] = outlier_mean + np.linalg.cholesky(R).dot(np.random.normal(size=k))
    elif i in [2, 3]:
      x[index] = mean + np.random.uniform(0, 1, size=k)
    else:
      x[index] = np.full((k, ), 0)
  return np.array(x)
X = random_vector_with_outliers(covariance, N)

np.savetxt("report2data.csv", X, delimiter=",")

xmean = np.mean(X, axis=0)
def mahalanobis(j):
  xnorm = (N*xmean - X[j])/(N-1) # mean of X with X[j] excluded
  sigma = np.matrix(
    np.sum( # np.outer(v1, v2) generates outer product of vectors v1 and v2
      map(lambda x: np.outer(x - xnorm, x - xnorm), np.delete(X, j, axis=0)), axis=0) / (N - 2))
  # matrix.get() returns this matrix inversed, i.e. 
  # sigma.dot(sigma.getI()) == np.eye((len(sigma), ))
  dmah = (X[j] - xmean).dot(sigma.getI()).dot(X[j] - xmean)
  return dmah

critical = stats.f.ppf(0.975, n, N-n)

print "critical value:\n{c}".format(c=critical)

for i in xrange(N):
  t = (N-n)*N*mahalanobis(i)/(n*(N*N-1))
  print t, "adopt" if t < critical else "reject {outlier}{x}".format(outlier=("outlier " if i in outliers else ""), x=X[i]), "outlier {x}".format(x=X[i]) if t < critical and i in outliers else ""
# bla

xmean_wo = np.mean(np.delete(X, outliers, axis=0), axis=0)
sigma_wo = np.matrix(
    np.sum( # np.outer(v1, v2) generates outer product of vectors v1 and v2
      map(lambda x: np.outer(x - xmean_wo, x - xmean_wo), 
          np.delete(X, outliers, axis=0)), axis=0) / (N - len(outliers) - 1))
sigma_wo_inv = sigma_wo.getI()
mahalanobis_without_outliers = lambda y: (y - xmean_wo).dot(sigma_wo_inv).dot(y - xmean_wo)
#

for i in xrange(N):
  t = (N-n)*N*mahalanobis_without_outliers(X[i])/(n*(N*N-1))
  print t, "adopt" if t < critical else "reject {outlier}{x}".format(outlier=("outlier " if i in outliers else ""), x=X[i]), "outlier {x}".format(x=X[i]) if t < critical and i in outliers else ""